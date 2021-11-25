import time
import certifi
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# Count the the number of records in the model data text file
def count_model_data():
    y = 0
    txt_in = open("demofile2.txt", 'r')
    for idx, x in enumerate(txt_in):
        y = idx
    txt_in.close()
    return y

# Open text file of model data and calculate male, female and total detections
# The first time the program is run, calculate all data in text file, any time after that, calculate only new entry data
def model_data_parse(all_chr_data, user_col, client_ID, after_first, start_from):
    m_det = 0
    f_det = 0
    age_demo = [0] * 6

    # Open model data and process it noting number of total, male and female detections, and age demographic
    # Arrange age related data into a list
    txt_in = open("demofile2.txt", 'r')
    if after_first == 0:
        for idx, x in enumerate(txt_in):
            model_rec = x.split(',')
            if "Male" in x:
                m_det = m_det + 1
            if "Female" in x:
                f_det = f_det + 1
            if int(model_rec[1]) <= 10:
                age_demo[0] = age_demo[0] + 1
            if 11 <= int(model_rec[1]) <= 20:
                age_demo[1] = age_demo[1] + 1
            if 21 <= int(model_rec[1]) <= 40:
                age_demo[2] = age_demo[2] + 1
            if 41 <= int(model_rec[1]) <= 60:
                age_demo[3] = age_demo[3] + 1
            if 61 <= int(model_rec[1]) <= 70:
                age_demo[4] = age_demo[4] + 1
            if int(model_rec[1]) > 70:
                age_demo[5] = age_demo[5] + 1
        total_det = m_det + f_det
    else:
        for idx, x in enumerate(txt_in):
            if idx > start_from:
                model_rec = x.split(',')
                if "Male" in x:
                    m_det = m_det + 1
                if "Female" in x:
                    f_det = f_det + 1
                if int(model_rec[1]) <= 10:
                    age_demo[0] = age_demo[0] + 1
                if 11 <= int(model_rec[1]) <= 20:
                    age_demo[1] = age_demo[1] + 1
                if 21 <= int(model_rec[1]) <= 40:
                    age_demo[2] = age_demo[2] + 1
                if 41 <= int(model_rec[1]) <= 60:
                    age_demo[3] = age_demo[3] + 1
                if 61 <= int(model_rec[1]) <= 70:
                    age_demo[4] = age_demo[4] + 1
                if int(model_rec[1]) > 70:
                    age_demo[5] = age_demo[5] + 1
        total_det = m_det + f_det
    txt_in.close()

    # Checking current month to update only current months data
    curr_month = datetime.now().month

    # Updating a users chart data by increasing the value of that users current chart data in Mongo Atlas
    x = 0
    for i in range(20):
        if i == (curr_month-1):
           c_m_data = "chart_data." + str(i) + ".male"
           c_f_data = "chart_data." + str(i) + ".female"
           c_d_data = "chart_data." + str(i) + ".detections"
           user_col.update_one({"_id": ObjectId(client_ID)},{"$inc": {c_m_data: m_det}})
           user_col.update_one({"_id": ObjectId(client_ID)},{"$inc": {c_f_data: f_det}})
           user_col.update_one({"_id": ObjectId(client_ID)},{"$inc": {c_d_data: total_det}})
        if 12 <= i <= 17:
           c_a_data = "chart_data." + str(i) + ".detections"
           age = age_demo[x]
           user_col.update_one({"_id": ObjectId(client_ID)},{"$inc": {c_a_data: age}})
           x = x + 1
        if i == 18:
           c_gm_data = "chart_data." + str(i) + ".male"
           user_col.update_one({"_id": ObjectId(client_ID)},{"$inc": {c_gm_data: m_det}})
        if i == 19:
           c_gf_data = "chart_data." + str(i) + ".female"
           user_col.update_one({"_id": ObjectId(client_ID)},{"$inc": {c_gf_data: f_det}})


def main():
    inf_loop = True
    after_first = 0
    f_list = 0
    txt_idx = [0] * 2

    # Connection to Mongo Atlas database
    con_db = MongoClient('mongodb+srv://admin:admin@coralyze.o8xfk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tlsCAFile=certifi.where())
    atlas_db = con_db['myFirstDatabase']
    user_col = atlas_db['users']

    # Reading client ID from text file
    txt_in = open('client_ID.txt', 'r')
    client_ID = txt_in.read().replace('\n', '')
    txt_in.close()

    # While loop that retrieve user's chart data, appends it to a list, reads the model data text file, changes user's chart data and updates user's record in database
    # Only processing data if new entries to the textfile have been made
    while inf_loop == True:
        chart_data = user_col.find({"_id": ObjectId(client_ID)},{"_id": 0, "chart_data": 1})

        all_chr_data = []

        #User's chart data split to show which indexes relate to which charts on the front end website
        for data in chart_data:
            # Total detections chart data
            all_chr_data.append(data["chart_data"][0])
            all_chr_data.append(data["chart_data"][1])
            all_chr_data.append(data["chart_data"][2])
            all_chr_data.append(data["chart_data"][3])
            all_chr_data.append(data["chart_data"][4])
            all_chr_data.append(data["chart_data"][5])
            all_chr_data.append(data["chart_data"][6])
            all_chr_data.append(data["chart_data"][7])
            all_chr_data.append(data["chart_data"][8])
            all_chr_data.append(data["chart_data"][9])
            all_chr_data.append(data["chart_data"][10])
            all_chr_data.append(data["chart_data"][11])

            # Age demographic chart data
            all_chr_data.append(data["chart_data"][12])
            all_chr_data.append(data["chart_data"][13])
            all_chr_data.append(data["chart_data"][14])
            all_chr_data.append(data["chart_data"][15])
            all_chr_data.append(data["chart_data"][16])
            all_chr_data.append(data["chart_data"][17])

            # Gender demographic chart data
            all_chr_data.append(data["chart_data"][18])
            all_chr_data.append(data["chart_data"][19])

        # Counting last index of model data text file
        start_from = count_model_data()

        # Used to place previous number of entries and current number of entries of model data into list
        if f_list == 1:
            txt_idx[f_list] = start_from
        elif f_list == 0:
            txt_idx[f_list] = start_from

        #After the first time the program is run, it compares the previous last index to current last index of the model data
        if after_first > 0:
            if txt_idx[1] > txt_idx[0]:
                model_data_parse(all_chr_data, user_col, client_ID, after_first, txt_idx[0])
                print("Updated data...")
            elif txt_idx[0] > txt_idx[1]:
                model_data_parse(all_chr_data, user_col, client_ID, after_first, txt_idx[1])
                print("Updated data...")
            else:
                print("No new data...")
        else:
            model_data_parse(all_chr_data, user_col, client_ID, after_first, start_from)
            print("Analytics Start...")

        #Used to change which position in the list the new number of enteries is in
        if f_list == 1:
            f_list = 0
        elif f_list == 0:
            f_list = 1
        after_first = 1

        #Make program sleep so database and analytics program are some what in sync
        time.sleep(3.2)

if __name__ == '__main__':
    main()
