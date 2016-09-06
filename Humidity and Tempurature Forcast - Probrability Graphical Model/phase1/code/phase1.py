__author__ = 'Jiranun.J'
import csv
import numpy as np

data_path = 'intelLabDataProcessed/'
result_path = '../results/'
readings_per_day = 48
active_inference_budgets = [0, 5, 10, 20, 25]

### test ####
# readings_per_day = 3
# active_inference_budgets = [2]


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


def get_avg_and_var(data):
    number_of_days = len(data[0])/readings_per_day
    result = []
    for sensor in range(len(data)):
        each_sensor = []
        for t in range(readings_per_day):
            index_last_data = readings_per_day*number_of_days
            dat = np.array([float(data[sensor][ind]) for ind in range(t, index_last_data, readings_per_day)])
            each_sensor.append((np.mean(dat), np.var(dat)))
        result.append(each_sensor)
    return result


def get_actual_data_by_window(actual_data, butget):
    number_of_days = len(actual_data[0])/readings_per_day
    num_sensors = len(actual_data)
    result = np.zeros((num_sensors, number_of_days*readings_per_day))
    sen_indx = 0
    for t in range(number_of_days*readings_per_day):
        for _ in range(butget):
            result[sen_indx][t] = float(actual_data[sen_indx][t])
            sen_indx = (sen_indx + 1) % num_sensors
    return result


def get_actual_data_by_var(actual_data, mv, butget):
    number_of_days = len(actual_data[0])/readings_per_day
    num_sensors = len(actual_data)
    result = np.zeros((num_sensors, number_of_days*readings_per_day))
    for t in range(number_of_days*readings_per_day):
        reading = t % readings_per_day
        top_var_idx = sorted(range(len(mv)), key=lambda i: float(mv[i][reading][1]), reverse=True)[:butget]
        for sen_indx in top_var_idx:
            result[sen_indx][t] = float(actual_data[sen_indx][t])
    return result


def get_prediction(unpredicted_data, mv):
    predicted_data = unpredicted_data.copy()
    for sensor in range(len(predicted_data)):
        for t in range(len(predicted_data[0])):
            if predicted_data[sensor][t] == 0.:
                time = t % readings_per_day
                predicted_data[sensor][t] = mv[sensor][time][0]
    return predicted_data


def get_mean_absolute_error(predicted_data, test_data):
    total_error = 0.
    total_prediction = len(predicted_data)*len(predicted_data[0])
    for sensor in range(len(predicted_data)):
        for t in range(len(predicted_data[0])):
            total_error += abs(predicted_data[sensor][t]-float(test_data[sensor][t]))
    return total_error/float(total_prediction)


def get_results(train_data, test_data, budget, output_path = ''):
    mean_var = get_avg_and_var(train_data)
    unpredicted_data_w = get_actual_data_by_window(test_data, budget)
    unpredicted_data_v = get_actual_data_by_var(test_data, mean_var, budget)
    predicted_data_w = get_prediction(unpredicted_data_w, mean_var)
    predicted_data_v = get_prediction(unpredicted_data_v, mean_var)
    error_w = get_mean_absolute_error(predicted_data_w, test_data)
    error_v = get_mean_absolute_error(predicted_data_v, test_data)
    first_row = ['sensors','0.5','1.0','1.5','2.0','2.5','3.0','3.5','4.0','4.5','5.0','5.5','6.0','6.5','7.0','7.5','8.0','8.5','9.0','9.5','10.0','10.5','11.0','11.5','12.0','12.5','13.0','13.5','14.0','14.5','15.0','15.5','16.0','16.5','17.0','17.5','18.0','18.5','19.0','19.5','20.0','20.5','21.0','21.5','22.0','22.5','23.0','23.5','0.0','0.5','1.0','1.5','2.0','2.5','3.0','3.5','4.0','4.5','5.0','5.5','6.0','6.5','7.0','7.5','8.0','8.5','9.0','9.5','10.0','10.5','11.0','11.5','12.0','12.5','13.0','13.5','14.0','14.5','15.0','15.5','16.0','16.5','17.0','17.5','18.0','18.5','19.0','19.5','20.0','20.5','21.0','21.5','22.0','22.5','23.0','23.5','0.0']
    w_filename = output_path+'w'+str(budget)+'.csv'
    with open(w_filename, 'wb') as csvfile:
        write_file = csv.writer(csvfile, delimiter = ',')
        write_file.writerow(first_row)
        for sensor in range(len(predicted_data_w)):
            str_data = [str(i) for i in predicted_data_w[sensor]]
            str_data.insert(0, sensor)
            write_file.writerow(str_data)
        # print w_filename,'has been generated successfully.'

    v_filename = output_path+'v'+str(budget)+'.csv'
    with open(v_filename, 'wb') as csvfile:
        write_file = csv.writer(csvfile, delimiter = ',')
        write_file.writerow(first_row)
        for sensor in range(len(predicted_data_v)):
            str_data = [str(i) for i in predicted_data_v[sensor]]
            str_data.insert(0, sensor)
            write_file.writerow(str_data)
        # print v_filename,'has been generated successfully.'

    return error_w, error_v


################################################################################################

humid_train = read_csv('intelHumidityTrain.csv')
humid_test = read_csv('intelHumidityTest.csv')
temp_train = read_csv('intelTemperatureTrain.csv')
temp_test = read_csv('intelTemperatureTest.csv')

### test ###
# train1 = read_csv('train1.csv')
# test1 = read_csv('test1.csv')

mean_abs_err = []
for budget in active_inference_budgets:
    humid_err_w, humid_err_v = get_results(humid_train, humid_test, budget, result_path+'humidity/')
    temp_err_w, temp_err_v = get_results(temp_train, temp_test, budget, result_path+'temperature/')
    mean_abs_err.append([humid_err_w, humid_err_v, temp_err_w, temp_err_v])
    print 'Phase1_temp_'+str(budget)+' = [',temp_err_w,',',temp_err_v,']'
    print 'Phase1_humid_'+str(budget)+' = [',humid_err_w,',',humid_err_v,']'
    # test ##
    # err_w, err_v = get_results(train1, test1, budget)


with open('mean_abs_err.csv', 'wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(['','Humid Window','Humid Var','Temp Window', 'Temp Var'])
    for i in range(len(active_inference_budgets)):
        row = [active_inference_budgets[i]]
        row.extend(mean_abs_err[i])
        write_file.writerow(row)
