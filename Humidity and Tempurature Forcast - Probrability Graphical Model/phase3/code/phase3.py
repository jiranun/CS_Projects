__author__ = 'Jiranun.J'
import csv
import numpy as np
import os
from sklearn import linear_model
import matplotlib.pyplot as plt

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
# active_inference_budgets = [5]


#### test ####
# readings_per_day = 3
# active_inference_budgets = [0,1,3]

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

# get b0-b50, and sigma2
def get_params(x_prev, x_next):

    if len(x_prev) != len(x_next):
        return None, None

    clf = linear_model.LinearRegression()
    clf.fit(x_prev, x_next)
    betas = clf.coef_
    betas = betas.tolist()
    b0 = clf.intercept_

    predicted_x = []
    for x in x_prev:
        pred = b0
        for i,s in enumerate(x):
            pred += betas[i]*s
        predicted_x.append(pred)

    diffs = [x-x_next[i] for i,x in enumerate(predicted_x)]
    variance = np.var(diffs)
    all_betas = [b0]
    all_betas.extend(betas)
    return all_betas, variance


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


def get_all_params(data):
    num_sensors = len(data)
    number_of_days = len(data[0])/readings_per_day
    all_params = np.zeros((num_sensors,readings_per_day, num_sensors+2))

    for t in range(1, readings_per_day):
        for s in range(num_sensors):
            x_prev = [[float(data[s_prev][i-1]) for s_prev in range(num_sensors)] for i in range(t, readings_per_day*number_of_days, readings_per_day)]
            x_next = [float(data[s][i]) for i in range(t, readings_per_day*number_of_days, readings_per_day)]
            betas, sigma = get_params(x_prev, x_next)
            betas.append(sigma)
            all_params[s][t] = betas

    # for s in range(num_sensors):
    #     x_prev = [[float(data[s_prev][i]) for s_prev in range(num_sensors)] for i in range(0, readings_per_day*number_of_days-1)]
    #     x_next = [float(data[s][i]) for i in range(1, readings_per_day*number_of_days)]
    #     betas, sigma = get_params(x_prev, x_next)
    #     betas.append(sigma)
    #     all_params[s] = betas
    return all_params


def get_prediction(train_data, test_data, budget, sensor_params):
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

    for t in range(number_of_test_days*readings_per_day):
        param_t = t % readings_per_day
        # compute mean and variance of each sensor
        mean_var = []
        if param_t != 0:
            for s in range(num_sensors):
                b0 = sensor_params[s][param_t][0]
                sigma = sensor_params[s][param_t][num_sensors+1]
                m = b0
                for s_ in range(num_sensors):
                    m += result_var[s_][t-1]*sensor_params[s][param_t][s_+1] # b0 + s0b1 + s1b2 + ...
                v = sigma
                for s_ in range(num_sensors):
                    v += mv[s_][t-1][1]*(sensor_params[s][param_t][s_+1]**2) # sigma + v0b1^2 + v1b2^2 + ...
                mean_var.append([m,v])
        else:
            mean_var = mv1.copy()

        top_var_idxs = sorted(range(len(mean_var)), key=lambda sen: float(mean_var[sen][1]), reverse=True)[:budget]
        window = [(sen_indx+i)%num_sensors for i in range(budget)]
        # print
        # print 'mean_var', mean_var
        # print 'top_var', top_var_idxs


        # ### observation ###
        # prev_val_w = [result_win[i][t-1] for i in range(num_sensors)]
        # new_prev_val = prev_val_w[:]
        # for s in window:
        #     obsrv_val = float(test_data[s][t])
        #     result_win[s][t] = obsrv_val
        #     b0 = sensor_params[s][param_t][0]
        #
        #     for s_prev in range(num_sensors):
        #         if sensor_params[s][param_t][s+1] < 0.000001:
        #             new_val = prev_val_w[s_prev]
        #         else:
        #             new_val = obsrv_val - b0
        #             for s_other in range(num_sensors):
        #                 if s_other != s_prev:
        #                     new_val -= result_win[s_other][t-1]*sensor_params[s][param_t][s_other+1]
        #             new_val /= sensor_params[s][param_t][s+1]
        #
        #         if abs(new_val-prev_val_w[s_prev]) > abs(new_prev_val[s_prev]-prev_val_w[s_prev]):
        #             new_prev_val[s_prev] = new_val
        # for s in window:
        #     result_win[s][t-1] = new_prev_val[s]


        # prev_val_v = result_var[:][t-1]
        # for s in top_var_idxs:
        #     result_var[s][t] = float(test_data[s][t])
        #     mv[s][t] = [float(test_data[s][t]), 0.]


        for s in range(num_sensors):
            b0 = sensor_params[s][param_t][0]

            #### Window ####
            if s not in window:
                if param_t == 0:
                    result_win[s][t] = mv1[s][0]
                else:
                    res = b0
                    for s_ in range(num_sensors):
                        res += result_win[s_][t-1]*sensor_params[s][param_t][s_+1] # b0 + b1s0 + b2s1 + ...
                    result_win[s][t] = res
            else:
                result_win[s][t] = float(test_data[s][t])

            #### Variance ####
            if s not in top_var_idxs:
                if param_t == 0:
                    result_var[s][t] = mv1[s][0]
                    mv[s][t] = mv1[s]
                else:
                    res = b0
                    for s_ in range(num_sensors):
                        res += result_var[s_][t-1]*sensor_params[s][param_t][s_+1] # b0 + b1s0 + b2s1 + ...
                    result_var[s][t] = res
                    mv[s][t] = mean_var[s]
                # result_var[s][t] = 0
            else:
                result_var[s][t] = float(test_data[s][t])
                mv[s][t] = [float(test_data[s][t]), 0.]

        sen_indx = (sen_indx+budget) % num_sensors

    # print 'win\n'
    # for inf in result_win:
    #     print inf
    # print 'var\n', result_var
    return result_win, result_var


Phase1_temp_0 = [ 1.16690277778 , 1.16690277778 ]
Phase1_humid_0 = [ 3.47049305556 , 3.47049305556 ]
Phase1_temp_5 = [ 1.04932638889 , 0.965868055556 ]
Phase1_humid_5 = [ 3.11869444444 , 3.15956944444 ]
Phase1_temp_10 = [ 0.9376875 , 0.808354166667 ]
Phase1_humid_10 = [ 2.78196527778 , 2.84661805556 ]
Phase1_temp_20 = [ 0.692020833333 , 0.555506944444 ]
Phase1_humid_20 = [ 2.06980555556 , 2.172 ]
Phase1_temp_25 = [ 0.597076388889 , 0.432569444444 ]
Phase1_humid_25 = [ 1.75699305556 , 1.82060416667 ]

Phase1_temp = [Phase1_temp_0,Phase1_temp_5,Phase1_temp_10,Phase1_temp_20,Phase1_temp_25]
Phase1_humid = [Phase1_humid_0,Phase1_humid_5,Phase1_humid_10,Phase1_humid_20,Phase1_humid_25]

Phase2_temp_0 = [2.2235345424552762, 2.2235345424552762, 1.1669027777777778, 1.1669027777777778]
Phase2_humid_0 = [4.8580561317308657, 4.8580561317308657, 3.4704930555555635, 3.4704930555555635]
Phase2_temp_5 = [1.4484931462227855, 1.3681778975780949, 0.97719495663075673, 0.80802583058320832]
Phase2_humid_5 = [2.5325697018767332, 2.7930543583439569, 2.314065090125506, 2.1087023886042067]
Phase2_temp_10 = [0.85720424699470865, 0.92480584629244733, 0.57845202677439067, 0.58621564160856476]
Phase2_humid_10 = [1.4509611889999159, 1.7062176739532999, 1.2804022940101556, 1.4741686651004733]
Phase2_temp_20 = [0.39432303645477651, 0.43519610857764879, 0.28883302706842251, 0.30348448125696253]
Phase2_humid_20 = [0.66229019958533519, 0.76285007569166863, 0.71928013528764279, 0.74213124912969586]
Phase2_temp_25 = [0.26476830816674096, 0.32593939787790621, 0.22111015404446188, 0.23035658298232378]
Phase2_humid_25 = [0.43652167089151134, 0.56949696790981275, 0.51569783341046904, 0.57141472499529622]

Phase2_temp = [Phase2_temp_0,Phase2_temp_5,Phase2_temp_10,Phase2_temp_20,Phase2_temp_25]
Phase2_humid = [Phase2_humid_0,Phase2_humid_5,Phase2_humid_10,Phase2_humid_20,Phase2_humid_25]

# train1 = read_csv('train1.csv')
# test1 = read_csv('test1.csv')
# test_sensor = get_all_params(train1)
# print train1
# print test_sensor

humid_train = read_csv('intelHumidityTrain.csv')
humid_test = read_csv('intelHumidityTest.csv')
temp_train = read_csv('intelTemperatureTrain.csv')
temp_test = read_csv('intelTemperatureTest.csv')

temp_sensor_params = get_all_params(temp_train)
humid_sensor_params = get_all_params(humid_train)

for i,budget in enumerate(active_inference_budgets):
    print_writefile_result = False

    # w,v = get_prediction(train1, test1, budget, test_sensor)
    # print w
    # print
    # print v
    # print "test "+"w"+str(budget)+" error : ",get_mean_absolute_error(w, test1)
    # print "test "+"v"+str(budget)+" error : ",get_mean_absolute_error(v, test1)
    #
    w,v = get_prediction(temp_train, temp_test, budget, temp_sensor_params)
    writeFile(w, output_path+'temperature/'+'w'+str(budget)+'.csv',print_writefile_result)
    writeFile(v, output_path+'temperature/'+'v'+str(budget)+'.csv',print_writefile_result)
    print "temperature "+"w"+str(budget)+" error : ",get_mean_absolute_error(w, temp_test)
    print "temperature "+"v"+str(budget)+" error : ",get_mean_absolute_error(v, temp_test)

    x = ['P1-w', 'P1-v', 'P2-h-w', 'P2-h-v', 'P2-d-w', 'P2-d-v', 'P3-w', 'P3-v']
    range_x = [2*j-1 for j in range(len(x))]
    plt.clf()
    plot_name = 'Temperature Budget '+str(budget)
    plt.title(plot_name)
    y = Phase1_temp[i]
    y.extend(Phase2_temp[i])
    y.extend([get_mean_absolute_error(w, temp_test),get_mean_absolute_error(v, temp_test)])
    plt.bar(range_x, y, align='center', color='red')
    plt.ylabel('mean absolute error')
    # plt.ylim(min(y), max(y))
    plt.xticks(range_x, x, rotation=15)
    plt.savefig(plot_name+'.png')

    w,v = get_prediction(humid_train, humid_test, budget, humid_sensor_params)
    writeFile(w, output_path+'humidity/'+'w'+str(budget)+'.csv',print_writefile_result)
    writeFile(v, output_path+'humidity/'+'v'+str(budget)+'.csv',print_writefile_result)
    print "humidity "+"w"+str(budget)+" error : ",get_mean_absolute_error(w, humid_test)
    print "humidity "+"v"+str(budget)+" error : ",get_mean_absolute_error(v, humid_test)

    plt.clf()
    plot_name = 'Humidity Budget '+str(budget)
    plt.title(plot_name)
    y = Phase1_humid[i]
    y.extend(Phase2_humid[i])
    y.extend([get_mean_absolute_error(w, humid_test),get_mean_absolute_error(v, humid_test)])
    plt.bar(range_x, y, align='center')
    plt.ylabel('mean absolute error')
    # plt.ylim(min(y), max(y))
    plt.xticks(range_x, x,rotation=15)
    plt.savefig(plot_name+'.png')

