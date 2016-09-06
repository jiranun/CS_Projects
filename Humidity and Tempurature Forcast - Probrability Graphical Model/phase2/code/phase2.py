__author__ = 'Jiranun.J'
import csv
import numpy as np
import os
from sklearn import linear_model

output_path = os.getcwd()+'/results/'

if not os.path.exists(output_path):
    os.makedirs(output_path)
if not os.path.exists(output_path+'temperature/'):
    os.makedirs(output_path+'temperature/')
if not os.path.exists(output_path+'humidity/'):
    os.makedirs(output_path+'humidity/')


data_path = 'intelLabDataProcessed/'
readings_per_day = 48
active_inference_budgets = [0, 5, 10, 20, 25]

### test ####
# readings_per_day = 3
# active_inference_budgets = []

def read_csv(filename):
    data = []
    with open(data_path + filename, 'rb') as f:
        reader = csv.reader(f)
        ignore = True

        for row in reader:
            # ignore first line
            if ignore:
                ignore = False
                continue

            row = row[1:]
            data.append(row)
    return data

# get b0, b1, and sigma2
def get_params(x_prev, x_next):

    if len(x_prev) != len(x_next):
        return 0.,0.,0.

    x_prev2 = [[x] for x in x_prev]
    clf = linear_model.LinearRegression()
    clf.fit(x_prev2, x_next)
    betas = clf.coef_
    b1 = betas.tolist()[0]
    b0 = clf.intercept_
    predicted_x = [b0+b1*x for x in x_prev]
    diffs = [x-x_next[i] for i,x in enumerate(predicted_x)]
    variance = np.var(diffs)
    return b0, b1, variance

def get_prev_next(data):
    x_prev = []
    x_next = []
    for i in range(len(data)-1):
        x_prev.append(float(data[i]))
        x_next.append(float(data[i+1]))
    return x_prev, x_next

def get_mean_absolute_error(predicted_data, test_data):
    total_error = 0.
    total_prediction = len(predicted_data)*len(predicted_data[0])
    for sensor in range(len(predicted_data)):
        for t in range(len(predicted_data[0])):
            total_error += abs(predicted_data[sensor][t]-float(test_data[sensor][t]))
    return total_error/float(total_prediction)

def writeFile(predict, filefullname, print_res = False):
    first_row = ['sensors','0.5','1.0','1.5','2.0','2.5','3.0','3.5','4.0','4.5','5.0','5.5','6.0','6.5','7.0','7.5','8.0','8.5','9.0','9.5','10.0','10.5','11.0','11.5','12.0','12.5','13.0','13.5','14.0','14.5','15.0','15.5','16.0','16.5','17.0','17.5','18.0','18.5','19.0','19.5','20.0','20.5','21.0','21.5','22.0','22.5','23.0','23.5','0.0','0.5','1.0','1.5','2.0','2.5','3.0','3.5','4.0','4.5','5.0','5.5','6.0','6.5','7.0','7.5','8.0','8.5','9.0','9.5','10.0','10.5','11.0','11.5','12.0','12.5','13.0','13.5','14.0','14.5','15.0','15.5','16.0','16.5','17.0','17.5','18.0','18.5','19.0','19.5','20.0','20.5','21.0','21.5','22.0','22.5','23.0','23.5','0.0']
    with open(filefullname, 'wb') as csvfile:
        write_file = csv.writer(csvfile, delimiter = ',')
        write_file.writerow(first_row)
        for sensor in range(len(predict)):
            str_data = [str(i) for i in predict[sensor]]
            str_data.insert(0, sensor)
            write_file.writerow(str_data)
        if print_res:
            print filefullname,'has been generated successfully.'


############ Model 1 stationary at hour level ##############

def get_sensors_params_model1(data):
    sensor_params = []
    for i in range(len(data)):
        lst = data[i]
        x_prev, x_next = get_prev_next(lst)
        b0, b1, sigma = get_params(x_prev, x_next)
        # print b0, b1, sigma
        sensor_params.append([b0,b1,sigma])
    return sensor_params


def get_prediction_model1(train_data, test_data, budget):
    num_sensors = len(test_data)
    number_of_train_days = len(train_data[0])/readings_per_day
    number_of_test_days = len(test_data[0])/readings_per_day

    # First time-stamp
    mv1 = np.zeros((num_sensors,2))
    for s in range(num_sensors):
        dat = [float(train_data[s][j]) for j in range(0, readings_per_day*number_of_train_days, readings_per_day)]
        mv1[s] = [np.mean(dat), np.var(dat)]

    result_win = np.zeros((num_sensors, number_of_test_days*readings_per_day))
    result_var = np.zeros((num_sensors, number_of_test_days*readings_per_day))

    sen_indx = 0
    sensor_params = get_sensors_params_model1(train_data)
    mv = np.zeros((num_sensors, number_of_test_days*readings_per_day, 2))

    for t in range(number_of_test_days*readings_per_day):

        # compute mean and variance of each sensor
        mean_var = []
        if t != 0:
            for s in range(num_sensors):
                b0 = sensor_params[s][0]
                b1 = sensor_params[s][1]
                sigma = sensor_params[s][2]
                prev_node_val = result_var[s][t-1]
                prev_var = mv[s][t-1][1]
                m = b0+b1*prev_node_val
                v = sigma+prev_var*(b1**2)
                mean_var.append([m,v])
                # print sigma, prev_var,b0,b1,v
        else:
            mean_var = mv1.copy()


        top_var_idxs = sorted(range(len(mean_var)), key=lambda sen: float(mean_var[sen][1]), reverse=True)[:budget]
        # print
        # if budget == 5:
        #     print 'mean_var', mean_var
        #     print 'top_var', top_var_idxs
        for s in range(num_sensors):
            b0 = sensor_params[s][0]
            b1 = sensor_params[s][1]

            #### Window ####
            window = [(sen_indx+i)%num_sensors for i in range(budget)]

            if s in window:
                result_win[s][t] = float(test_data[s][t])
            else:
                if t == 0:
                    result_win[s][t] = mv1[s][0]
                else:
                    prev_node_val = result_win[s][t-1]
                    result_win[s][t] = b0 + prev_node_val*b1


            #### Variance ####
            if s in top_var_idxs:
                result_var[s][t] = float(test_data[s][t])
                mv[s][t] = [float(test_data[s][t]), 0.]
            else:
                if t == 0:
                    result_var[s][t] = mv1[s][0]
                    mv[s][t] = mv1[s]
                else:
                    prev_node_val = result_var[s][t-1]
                    result_var[s][t] = b0 + prev_node_val*b1
                    mv[s][t] = mean_var[s]

        # print 'win\n', result_win
        # print 'var\n',result_var

        sen_indx = (sen_indx+budget) % num_sensors

    return result_win, result_var


############ Model 2 stationary at the day level ##############

def get_sensors_params_model2(data):
    num_sensors = len(data)
    number_of_days = len(data[0])/readings_per_day
    sensor_params = np.zeros((num_sensors, readings_per_day, 3))
    for t in range(1, readings_per_day):
        for s in range(num_sensors):
            x_prev = [float(data[s][i-1]) for i in range(t, readings_per_day*number_of_days, readings_per_day)]
            x_next = [float(data[s][i]) for i in range(t, readings_per_day*number_of_days, readings_per_day)]
            b0, b1, sigma = get_params(x_prev, x_next)
            sensor_params[s][t] = [b0,b1,sigma]
    return sensor_params

def get_prediction_model2(train_data, test_data, budget):
    num_sensors = len(test_data)
    number_of_train_days = len(train_data[0])/readings_per_day
    number_of_test_days = len(test_data[0])/readings_per_day

    # First time-stamp
    mv1 = np.zeros((num_sensors, 2))
    for s in range(num_sensors):
        dat = [float(train_data[s][j]) for j in range(0, readings_per_day*number_of_train_days, readings_per_day)]
        mv1[s] = [np.mean(dat), np.var(dat)]

    result_win = np.zeros((num_sensors, number_of_test_days*readings_per_day))
    result_var = np.zeros((num_sensors, number_of_test_days*readings_per_day))
    mv = np.zeros((num_sensors, number_of_test_days*readings_per_day, 2))
    sen_indx = 0
    sensor_params = get_sensors_params_model2(train_data)

    for t in range(number_of_test_days*readings_per_day):
        param_t = t % readings_per_day

        # compute mean and variance of each sensor
        mean_var = []
        if param_t != 0:
            for s in range(num_sensors):
                b0 = sensor_params[s][param_t][0]
                b1 = sensor_params[s][param_t][1]
                sigma = sensor_params[s][param_t][2]
                prev_node_val = result_var[s][t-1]
                prev_var = mv[s][t-1][1]
                m = b0+b1*prev_node_val
                v = sigma+prev_var*(b1**2)
                mean_var.append([m,v])
        else:
            mean_var = mv1.copy()

        top_var_idxs = sorted(range(len(mean_var)), key=lambda sen: float(mean_var[sen][1]), reverse=True)[:budget]
        # print
        # print 'mean_var', mean_var
        # print 'top_var', top_var_idxs
        for s in range(num_sensors):
            b0 = sensor_params[s][param_t][0]
            b1 = sensor_params[s][param_t][1]

            #### Window ####
            window = [(sen_indx+i)%num_sensors for i in range(budget)]

            if s in window:
                result_win[s][t] = float(test_data[s][t])
            else:
                if param_t == 0:
                    result_win[s][t] = mv1[s][0]
                else:
                    prev_node_val = result_win[s][t-1]
                    result_win[s][t] = b0 + prev_node_val*b1
                # result_win[s][t] = 0


            #### Variance ####
            if s in top_var_idxs:
                result_var[s][t] = float(test_data[s][t])
                mv[s][t] = [float(test_data[s][t]), 0.]
            else:
                if param_t == 0:
                    result_var[s][t] = mv1[s][0]
                    mv[s][t] = mv1[s]
                else:
                    prev_node_val = result_var[s][t-1]
                    result_var[s][t] = b0 + prev_node_val*b1
                    mv[s][t] = mean_var[s]
                # result_var[s][t] = 0

        sen_indx = (sen_indx+budget) % num_sensors
        # print 'win\n', result_win
        # print 'var\n', result_var
    return result_win, result_var

humid_train = read_csv('intelHumidityTrain.csv')
humid_test = read_csv('intelHumidityTest.csv')
temp_train = read_csv('intelTemperatureTrain.csv')
temp_test = read_csv('intelTemperatureTest.csv')
#
# train1 = read_csv('train1.csv')
# test1 = read_csv('test1.csv')

for budget in active_inference_budgets:
    print_writefile_result = False

    # w,v = get_prediction_model1(train1, test1, budget)
    # print w
    # print
    # print v
    # writeFile(w, 'd-w'+str(budget)+'.csv',print_writefile_result)
    # writeFile(v, 'd-v'+str(budget)+'.csv',print_writefile_result)
    # print 'err(d-w) =', get_mean_absolute_error(w,test1)
    # print 'err(d-v) =', get_mean_absolute_error(v,test1)
    # w,v = get_prediction_model2(train1, test1, budget)
    # writeFile(w, 'h-w'+str(budget)+'.csv',print_writefile_result)
    # writeFile(v, 'h-v'+str(budget)+'.csv',print_writefile_result)
    # print 'err(h-w) =', get_mean_absolute_error(w,test1)
    # print 'err(h-v) =', get_mean_absolute_error(v,test1)
    # print w
    # print
    # print v

    err_temp = []
    err_humid = []

    w,v = get_prediction_model1(temp_train, temp_test, budget)
    writeFile(w, output_path+'temperature/'+'h-w'+str(budget)+'.csv',print_writefile_result)
    writeFile(v, output_path+'temperature/'+'h-v'+str(budget)+'.csv',print_writefile_result)
    # print "temperature "+"d-w"+str(budget)+" error :",get_mean_absolute_error(w, temp_test)
    # print "temperature "+"d-v"+str(budget)+" error : ",get_mean_absolute_error(v, temp_test)
    # print
    err_temp.append(get_mean_absolute_error(w, temp_test))
    err_temp.append(get_mean_absolute_error(v, temp_test))

    w,v = get_prediction_model2(temp_train, temp_test, budget)
    writeFile(w, output_path+'temperature/'+'d-w'+str(budget)+'.csv',print_writefile_result)
    writeFile(v, output_path+'temperature/'+'d-v'+str(budget)+'.csv',print_writefile_result)
    # print "temperature "+"h-w"+str(budget)+" error : ",get_mean_absolute_error(w, temp_test)
    # print "temperature "+"h-v"+str(budget)+" error : ",get_mean_absolute_error(v, temp_test)
    # print
    err_temp.append(get_mean_absolute_error(w, temp_test))
    err_temp.append(get_mean_absolute_error(v, temp_test))

    w,v = get_prediction_model1(humid_train, humid_test, budget)
    writeFile(w, output_path+'humidity/'+'h-w'+str(budget)+'.csv',print_writefile_result)
    writeFile(v, output_path+'humidity/'+'h-v'+str(budget)+'.csv',print_writefile_result)
    # print "humidity "+"d-w"+str(budget)+" error : ",get_mean_absolute_error(w, humid_test)
    # print "humidity "+"d-v"+str(budget)+" error : ",get_mean_absolute_error(v, humid_test)
    # print
    err_humid.append(get_mean_absolute_error(w, humid_test))
    err_humid.append(get_mean_absolute_error(v, humid_test))

    w,v = get_prediction_model2(humid_train, humid_test, budget)
    writeFile(w, output_path+'humidity/'+'d-w'+str(budget)+'.csv',print_writefile_result)
    writeFile(v, output_path+'humidity/'+'d-v'+str(budget)+'.csv',print_writefile_result)
    # print "humidity "+"h-w"+str(budget)+" error : ",get_mean_absolute_error(w, humid_test)
    # print "humidity "+"h-v"+str(budget)+" error : ",get_mean_absolute_error(v, humid_test)
    # print
    err_humid.append(get_mean_absolute_error(w, humid_test))
    err_humid.append(get_mean_absolute_error(v, humid_test))


    print 'Phase2_temp_'+str(budget)+' =',err_temp
    print 'Phase2_humid_'+str(budget)+' =',err_humid



