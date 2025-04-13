# Demonstration Exercises 5

## Usage and sample output:
### Exercise 1
```sh
$ python src/simulation/demo_5/server_system.py --exercise 1 --number-of-simulations 100
INFO - Starting 100 simulations...
INFO - Completed 100 simulations.
INFO - Average number of customers served: 90.87 (std: 9.47)
INFO - Average end of service time: 9.15 (std: 0.23)
INFO - Average spent time: 0.22 (std: 0.085)
INFO - Average number of customers served on server 0: 90.87 (std: 9.47), ratio: 1.0000
INFO - Simulation completed.

$ python src/simulation/demo_5/server_system.py --exercise 1 --number-of-simulations 1000
INFO - Starting 1000 simulations...
INFO - Completed 1000 simulations.
INFO - Average number of customers served: 89.97 (std: 9.68)
INFO - Average end of service time: 9.12 (std: 0.22)
INFO - Average spent time: 0.21 (std: 0.082)
INFO - Average number of customers served on server 0: 89.97 (std: 9.68), ratio: 1.0000
INFO - Simulation completed.
```


### Exercise 2
```sh
$ python src/simulation/demo_5/server_system.py --exercise 2 --number-of-simulations 100
INFO - Starting 100 simulations...
INFO - Completed 100 simulations.
INFO - Average number of customers served: 54.88 (std: 7.20)
INFO - Average end of service time: 9.78 (std: 0.73)
INFO - Average spent time: 0.61 (std: 0.32)
INFO - Average number of customers served on server 0: 32.06 (std: 5.52), ratio: 0.5842
INFO - Average number of customers served on server 1: 22.82 (std: 4.34), ratio: 0.4158
INFO - Simulation completed.

$ python src/simulation/demo_5/server_system.py --exercise 2 --number-of-simulations 1000
INFO - Starting 1000 simulations...
INFO - Completed 1000 simulations.
INFO - Average number of customers served: 54.09 (std: 7.30)
INFO - Average end of service time: 9.85 (std: 0.82)
INFO - Average spent time: 0.68 (std: 0.37)
INFO - Average number of customers served on server 0: 31.54 (std: 5.06), ratio: 0.5831
INFO - Average number of customers served on server 1: 22.55 (std: 4.76), ratio: 0.4169
INFO - Simulation completed.
```

Logs with debug-level enabled during a single simulation run:
```log
INFO - Starting 1 simulations...
INFO - Starting simulation...
DEBUG - 0.1133: #0 arrives
DEBUG - 0.1133: #0 starts service on server 0
DEBUG - 0.1183: #0 ends service on server 0
DEBUG - 0.2833: #1 arrives
DEBUG - 0.2833: #1 starts service on server 0
DEBUG - 0.2836: #2 arrives
DEBUG - 0.2836: #2 starts service on server 1
DEBUG - 0.4208: #1 ends service on server 0
DEBUG - 0.5082: #2 ends service on server 1
DEBUG - 0.5553: #3 arrives
DEBUG - 0.5553: #3 starts service on server 0
DEBUG - 0.6812: #4 arrives
DEBUG - 0.6812: #4 starts service on server 1
DEBUG - 1.2595: #3 ends service on server 0
DEBUG - 1.6908: #5 arrives
DEBUG - 1.6908: #5 starts service on server 0
DEBUG - 1.6910: #6 arrives
DEBUG - 1.7031: #7 arrives
DEBUG - 1.7766: #4 ends service on server 1
DEBUG - 1.7766: #6 starts service on server 1
DEBUG - 1.8813: #8 arrives
DEBUG - 2.0596: #6 ends service on server 1
DEBUG - 2.0596: #7 starts service on server 1
DEBUG - 2.1776: #7 ends service on server 1
DEBUG - 2.1776: #8 starts service on server 1
DEBUG - 2.2581: #5 ends service on server 0
DEBUG - 2.2800: #8 ends service on server 1
DEBUG - 2.4063: #9 arrives
DEBUG - 2.4063: #9 starts service on server 0
DEBUG - 2.4156: #9 ends service on server 0
DEBUG - 2.6550: #10 arrives
DEBUG - 2.6550: #10 starts service on server 0
DEBUG - 2.6776: #11 arrives
DEBUG - 2.6776: #11 starts service on server 1
DEBUG - 2.8067: #12 arrives
DEBUG - 2.8756: #13 arrives
DEBUG - 2.9126: #10 ends service on server 0
DEBUG - 2.9126: #12 starts service on server 0
DEBUG - 2.9503: #14 arrives
DEBUG - 3.2378: #15 arrives
DEBUG - 3.2568: #11 ends service on server 1
DEBUG - 3.2568: #13 starts service on server 1
DEBUG - 3.2918: #16 arrives
DEBUG - 3.3271: #13 ends service on server 1
DEBUG - 3.3271: #14 starts service on server 1
DEBUG - 3.3756: #12 ends service on server 0
DEBUG - 3.3756: #15 starts service on server 0
DEBUG - 3.4956: #17 arrives
DEBUG - 3.5065: #14 ends service on server 1
DEBUG - 3.5065: #16 starts service on server 1
DEBUG - 3.5893: #15 ends service on server 0
DEBUG - 3.5893: #17 starts service on server 0
DEBUG - 3.6704: #18 arrives
DEBUG - 3.6960: #19 arrives
DEBUG - 3.9172: #16 ends service on server 1
DEBUG - 3.9172: #18 starts service on server 1
DEBUG - 3.9403: #20 arrives
DEBUG - 4.2567: #21 arrives
DEBUG - 4.2920: #18 ends service on server 1
DEBUG - 4.2920: #19 starts service on server 1
DEBUG - 4.3213: #17 ends service on server 0
DEBUG - 4.3213: #20 starts service on server 0
DEBUG - 4.3565: #22 arrives
DEBUG - 4.4006: #23 arrives
DEBUG - 4.4482: #19 ends service on server 1
DEBUG - 4.4482: #21 starts service on server 1
DEBUG - 4.4835: #21 ends service on server 1
DEBUG - 4.4835: #22 starts service on server 1
DEBUG - 4.5249: #24 arrives
DEBUG - 4.5256: #20 ends service on server 0
DEBUG - 4.5256: #23 starts service on server 0
DEBUG - 4.6636: #23 ends service on server 0
DEBUG - 4.6636: #24 starts service on server 0
DEBUG - 4.9048: #25 arrives
DEBUG - 4.9227: #26 arrives
DEBUG - 4.9693: #27 arrives
DEBUG - 5.0189: #28 arrives
DEBUG - 5.0325: #22 ends service on server 1
DEBUG - 5.0325: #25 starts service on server 1
DEBUG - 5.1461: #29 arrives
DEBUG - 5.2354: #30 arrives
DEBUG - 5.2562: #31 arrives
DEBUG - 5.3444: #25 ends service on server 1
DEBUG - 5.3444: #26 starts service on server 1
DEBUG - 5.4543: #24 ends service on server 0
DEBUG - 5.4543: #27 starts service on server 0
DEBUG - 5.4827: #27 ends service on server 0
DEBUG - 5.4827: #28 starts service on server 0
DEBUG - 5.5103: #26 ends service on server 1
DEBUG - 5.5103: #29 starts service on server 1
DEBUG - 5.5892: #32 arrives
DEBUG - 5.6091: #29 ends service on server 1
DEBUG - 5.6091: #30 starts service on server 1
DEBUG - 5.6585: #33 arrives
DEBUG - 5.6755: #28 ends service on server 0
DEBUG - 5.6755: #31 starts service on server 0
DEBUG - 5.6931: #30 ends service on server 1
DEBUG - 5.6931: #32 starts service on server 1
DEBUG - 5.7253: #32 ends service on server 1
DEBUG - 5.7253: #33 starts service on server 1
DEBUG - 5.7444: #34 arrives
DEBUG - 5.9249: #31 ends service on server 0
DEBUG - 5.9249: #34 starts service on server 0
DEBUG - 6.1195: #33 ends service on server 1
DEBUG - 6.1411: #34 ends service on server 0
DEBUG - 6.2244: #35 arrives
DEBUG - 6.2244: #35 starts service on server 0
DEBUG - 6.3511: #35 ends service on server 0
DEBUG - 6.8406: #36 arrives
DEBUG - 6.8406: #36 starts service on server 0
DEBUG - 7.0550: #37 arrives
DEBUG - 7.0550: #37 starts service on server 1
DEBUG - 7.1960: #38 arrives
DEBUG - 7.2961: #39 arrives
DEBUG - 7.3030: #37 ends service on server 1
DEBUG - 7.3030: #38 starts service on server 1
DEBUG - 7.3082: #40 arrives
DEBUG - 7.3454: #36 ends service on server 0
DEBUG - 7.3454: #39 starts service on server 0
DEBUG - 7.4758: #39 ends service on server 0
DEBUG - 7.4758: #40 starts service on server 0
DEBUG - 7.5866: #41 arrives
DEBUG - 7.7557: #42 arrives
DEBUG - 7.7577: #43 arrives
DEBUG - 7.9146: #40 ends service on server 0
DEBUG - 7.9146: #41 starts service on server 0
DEBUG - 7.9861: #44 arrives
DEBUG - 8.0703: #45 arrives
DEBUG - 8.0725: #46 arrives
DEBUG - 8.2680: #41 ends service on server 0
DEBUG - 8.2680: #42 starts service on server 0
DEBUG - 8.5280: #47 arrives
DEBUG - 8.7872: #38 ends service on server 1
DEBUG - 8.7872: #43 starts service on server 1
DEBUG - 8.7898: #42 ends service on server 0
DEBUG - 8.7898: #44 starts service on server 0
DEBUG - 8.8024: #43 ends service on server 1
DEBUG - 8.8024: #45 starts service on server 1
DEBUG - 9.5123: #44 ends service on server 0
DEBUG - 9.5123: #46 starts service on server 0
DEBUG - 9.6839: #45 ends service on server 1
DEBUG - 9.6839: #47 starts service on server 1
DEBUG - 10.3087: #46 ends service on server 0
DEBUG - 10.4134: #47 ends service on server 1
INFO - Total customers served: 48
INFO - End of service time: 10.41
INFO - Average spent time: 0.63
INFO - Customers per server: [24, 24]
INFO - Completed 1 simulations.
INFO - Average number of customers served: 48.00 (std: 0.00)
INFO - Average end of service time: 10.41 (std: 0.00)
INFO - Average spent time: 0.63 (std: 0.0)
INFO - Average number of customers served on server 0: 24.00 (std: 0.00), ratio: 0.5000
INFO - Average number of customers served on server 1: 24.00 (std: 0.00), ratio: 0.5000
INFO - Simulation completed.
```
