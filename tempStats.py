import sys
import pandas
import os

def packetSummary(packet_path, init_step):
    packet_means = []

    for i in range(0,10):
        file_path = "{0}{1}.csv".format(packet_path,i)
        if os.path.isfile(file_path):

            packet_file = pandas.read_csv(file_path)
            sum_legal_sent = sum(packet_file.LegalSent[init_step:])
            sum_legal_received = sum(packet_file.LegalReceived[init_step:])

            temp_average = (sum_legal_received/sum_legal_sent)
            packet_means.append(temp_average)

    average = sum(packet_means)/len(packet_means)
    print("n = {0} m = {1}".format(len(packet_means), average))

packet_path = sys.argv[1]
packetSummary(packet_path, 10)

