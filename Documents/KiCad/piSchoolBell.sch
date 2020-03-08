EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L My_RaspberryPi:Raspberry_Pi_2_3_all_pin_ordered J3
U 1 1 5E636C40
P 5850 3800
F 0 "J3" H 5850 5167 50  0000 C CNN
F 1 "Raspberry_Pi_2_3_all_pin_ordered" H 5850 5076 50  0000 C CNN
F 2 "My_RaspberryPi:RaspberryPi_Hat_2x20_pin_GPIO_larger_pads" H 5850 3800 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 5850 3800 50  0001 C CNN
	1    5850 3800
	1    0    0    -1  
$EndComp
$Comp
L My_Headers:ZS-042_4-pin_RTC_Module J1
U 1 1 5E649AFE
P 3450 2900
F 0 "J1" H 3413 2505 50  0000 C CNN
F 1 "ZS-042_4-pin_RTC_Module" H 3413 2596 50  0000 C CNN
F 2 "My_Parts:ZS-042_RTC_Module_larger_pads" H 3450 2900 50  0001 C CNN
F 3 "~" H 3450 2900 50  0001 C CNN
	1    3450 2900
	-1   0    0    1   
$EndComp
Wire Wire Line
	5050 2900 3650 2900
Wire Wire Line
	3650 3000 5050 3000
$Comp
L My_Headers:10-pin_header_LCD_interface J2
U 1 1 5E66E013
P 3450 3950
F 0 "J2" H 3442 3135 50  0000 C CNN
F 1 "10-pin_header_LCD_interface" H 3442 3226 50  0000 C CNN
F 2 "My_Headers:10-pin_LCD_header_larger_pads" H 3350 3350 50  0001 C CNN
F 3 "~" H 3900 3900 50  0001 C CNN
	1    3450 3950
	-1   0    0    1   
$EndComp
Wire Wire Line
	3650 3550 4350 3550
Wire Wire Line
	4350 3550 4350 3300
Wire Wire Line
	4350 3300 5050 3300
Wire Wire Line
	3650 3650 4450 3650
Wire Wire Line
	4450 3650 4450 3400
Wire Wire Line
	4450 3400 5050 3400
Wire Wire Line
	3650 3750 4550 3750
Wire Wire Line
	4550 3750 4550 3500
Wire Wire Line
	4550 3500 5050 3500
Wire Wire Line
	3650 3850 4650 3850
Wire Wire Line
	4650 3850 4650 3700
Wire Wire Line
	4650 3700 5050 3700
Wire Wire Line
	3650 3950 4750 3950
Wire Wire Line
	4750 3950 4750 3800
Wire Wire Line
	4750 3800 5050 3800
Wire Wire Line
	3650 4050 4850 4050
Wire Wire Line
	4850 4050 4850 3900
Wire Wire Line
	4850 3900 5050 3900
Wire Wire Line
	3650 4150 4100 4150
Wire Wire Line
	3650 2800 4100 2800
$Comp
L My_Headers:3-pin_KY-019_relay_header J4
U 1 1 5E67312D
P 9900 3300
F 0 "J4" H 10069 3315 50  0000 L CNN
F 1 "3-pin_KY-019_relay_header" H 9900 3100 50  0001 C CNN
F 2 "My_Headers:3-pin_KY-019_Relay_header_larger_pads" H 9900 3000 50  0001 C CNN
F 3 "~" H 9900 3300 50  0001 C CNN
	1    9900 3300
	1    0    0    -1  
$EndComp
$Comp
L My_Headers:2-pin_NO_switch_header J5
U 1 1 5E675D31
P 9900 3600
F 0 "J5" H 9988 3530 50  0000 L CNN
F 1 "2-pin_NO_switch_header" H 9900 3400 50  0001 C CNN
F 2 "My_Headers:2-pin_NO_switch_header_larger_pads" H 9950 3300 50  0001 C CNN
F 3 "~" H 9900 3600 50  0001 C CNN
	1    9900 3600
	1    0    0    -1  
$EndComp
$Comp
L My_Headers:2-pin_NO_switch_header J6
U 1 1 5E677463
P 9900 4050
F 0 "J6" H 9988 3980 50  0000 L CNN
F 1 "2-pin_NO_switch_header" H 9900 3850 50  0001 C CNN
F 2 "My_Headers:2-pin_NO_switch_header_larger_pads" H 9950 3750 50  0001 C CNN
F 3 "~" H 9900 4050 50  0001 C CNN
	1    9900 4050
	1    0    0    -1  
$EndComp
$Comp
L My_Headers:2-pin_NO_switch_header J7
U 1 1 5E677CFE
P 9900 4450
F 0 "J7" H 9988 4380 50  0000 L CNN
F 1 "2-pin_NO_switch_header" H 9900 4250 50  0001 C CNN
F 2 "My_Headers:2-pin_NO_switch_header_larger_pads" H 9950 4150 50  0001 C CNN
F 3 "~" H 9900 4450 50  0001 C CNN
	1    9900 4450
	1    0    0    -1  
$EndComp
$Comp
L My_Headers:2-pin_NO_switch_header J8
U 1 1 5E678561
P 9900 4850
F 0 "J8" H 9988 4780 50  0000 L CNN
F 1 "2-pin_NO_switch_header" H 9900 4650 50  0001 C CNN
F 2 "My_Headers:2-pin_NO_switch_header_larger_pads" H 9950 4550 50  0001 C CNN
F 3 "~" H 9900 4850 50  0001 C CNN
	1    9900 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	9700 3600 9100 3600
Wire Wire Line
	9100 3600 9100 4050
Wire Wire Line
	9100 4850 9700 4850
Connection ~ 9100 4450
Wire Wire Line
	9100 4450 9100 4850
Wire Wire Line
	9700 4050 9100 4050
Connection ~ 9100 4050
Wire Wire Line
	9100 4050 9100 4450
$Comp
L Device:R R1
U 1 1 5E67AD35
P 7900 3700
F 0 "R1" V 7693 3700 50  0000 C CNN
F 1 "300R" V 7784 3700 50  0000 C CNN
F 2 "My_Misc:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal_larger_pads" V 7830 3700 50  0001 C CNN
F 3 "~" H 7900 3700 50  0001 C CNN
	1    7900 3700
	0    1    1    0   
$EndComp
$Comp
L Device:R R2
U 1 1 5E67C069
P 7900 4150
F 0 "R2" V 7693 4150 50  0000 C CNN
F 1 "300R" V 7784 4150 50  0000 C CNN
F 2 "My_Misc:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal_larger_pads" V 7830 4150 50  0001 C CNN
F 3 "~" H 7900 4150 50  0001 C CNN
	1    7900 4150
	0    1    1    0   
$EndComp
$Comp
L Device:R R3
U 1 1 5E67CAE3
P 7900 4550
F 0 "R3" V 7693 4550 50  0000 C CNN
F 1 "300R" V 7784 4550 50  0000 C CNN
F 2 "My_Misc:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal_larger_pads" V 7830 4550 50  0001 C CNN
F 3 "~" H 7900 4550 50  0001 C CNN
	1    7900 4550
	0    1    1    0   
$EndComp
$Comp
L Device:R R4
U 1 1 5E67D536
P 7900 4950
F 0 "R4" V 7693 4950 50  0000 C CNN
F 1 "300R" V 7784 4950 50  0000 C CNN
F 2 "My_Misc:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal_larger_pads" V 7830 4950 50  0001 C CNN
F 3 "~" H 7900 4950 50  0001 C CNN
	1    7900 4950
	0    1    1    0   
$EndComp
Wire Wire Line
	9700 3700 8200 3700
Wire Wire Line
	7750 3700 7300 3700
Wire Wire Line
	7300 3700 7300 3300
Wire Wire Line
	7300 3300 6650 3300
Wire Wire Line
	6650 3500 7200 3500
Wire Wire Line
	7200 3500 7200 4150
Wire Wire Line
	7200 4150 7750 4150
Wire Wire Line
	8050 4150 8200 4150
Wire Wire Line
	9100 4450 9700 4450
Wire Wire Line
	9700 4550 8200 4550
Wire Wire Line
	7750 4550 7000 4550
Wire Wire Line
	7000 4550 7000 3600
Wire Wire Line
	7000 3600 6650 3600
Wire Wire Line
	9700 4950 8200 4950
Wire Wire Line
	7750 4950 6900 4950
Wire Wire Line
	6900 4950 6900 3800
Wire Wire Line
	6900 3800 6650 3800
Wire Wire Line
	9700 3300 9350 3300
Wire Wire Line
	9350 3300 9350 2800
Wire Wire Line
	6650 2800 9350 2800
Wire Wire Line
	4100 2050 9350 2050
$Comp
L Device:R R5
U 1 1 5E6A51B6
P 8550 3600
F 0 "R5" V 8343 3600 50  0000 C CNN
F 1 "10k" V 8434 3600 50  0000 C CNN
F 2 "My_Misc:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal_larger_pads" V 8480 3600 50  0001 C CNN
F 3 "~" H 8550 3600 50  0001 C CNN
	1    8550 3600
	0    1    1    0   
$EndComp
$Comp
L Device:R R6
U 1 1 5E6A7537
P 8550 4050
F 0 "R6" V 8343 4050 50  0000 C CNN
F 1 "10k" V 8434 4050 50  0000 C CNN
F 2 "My_Misc:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal_larger_pads" V 8480 4050 50  0001 C CNN
F 3 "~" H 8550 4050 50  0001 C CNN
	1    8550 4050
	0    1    1    0   
$EndComp
$Comp
L Device:R R7
U 1 1 5E6A8664
P 8550 4450
F 0 "R7" V 8343 4450 50  0000 C CNN
F 1 "10k" V 8434 4450 50  0000 C CNN
F 2 "My_Misc:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal_larger_pads" V 8480 4450 50  0001 C CNN
F 3 "~" H 8550 4450 50  0001 C CNN
	1    8550 4450
	0    1    1    0   
$EndComp
$Comp
L Device:R R8
U 1 1 5E6AA5F9
P 8550 4850
F 0 "R8" V 8343 4850 50  0000 C CNN
F 1 "10k" V 8434 4850 50  0000 C CNN
F 2 "My_Misc:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal_larger_pads" V 8480 4850 50  0001 C CNN
F 3 "~" H 8550 4850 50  0001 C CNN
	1    8550 4850
	0    1    1    0   
$EndComp
Wire Wire Line
	9700 3400 8900 3400
Wire Wire Line
	8900 3400 8900 3600
Wire Wire Line
	8900 3600 8700 3600
Wire Wire Line
	8900 4850 8700 4850
Connection ~ 8900 4450
Wire Wire Line
	8900 4450 8900 4850
Wire Wire Line
	8700 4050 8900 4050
Connection ~ 8900 4050
Wire Wire Line
	8900 4050 8900 4450
Wire Wire Line
	8900 3600 8900 4050
Connection ~ 8900 3600
Wire Wire Line
	8700 4450 8900 4450
Wire Wire Line
	8200 4450 8200 4550
Connection ~ 8200 4550
Wire Wire Line
	8200 4550 8050 4550
Wire Wire Line
	8200 4450 8400 4450
Wire Wire Line
	8200 4950 8200 4850
Wire Wire Line
	8200 4850 8400 4850
Connection ~ 8200 4950
Wire Wire Line
	8200 4950 8050 4950
Wire Wire Line
	8200 4150 8200 4050
Wire Wire Line
	8200 4050 8400 4050
Connection ~ 8200 4150
Wire Wire Line
	8200 4150 9700 4150
Wire Wire Line
	8200 3700 8200 3600
Wire Wire Line
	8200 3600 8400 3600
Connection ~ 8200 3700
Wire Wire Line
	8200 3700 8050 3700
Wire Wire Line
	3650 4250 4000 4250
Wire Wire Line
	4950 4250 4950 4000
Wire Wire Line
	4950 4000 5050 4000
Connection ~ 4000 4250
Wire Wire Line
	4000 4250 4950 4250
Wire Wire Line
	3650 2700 4000 2700
Wire Wire Line
	5050 2800 4700 2800
Wire Wire Line
	4700 2150 9100 2150
Wire Wire Line
	9350 2050 9350 2800
Connection ~ 9350 2800
Connection ~ 9100 3600
Wire Wire Line
	9100 2150 9100 3600
Wire Wire Line
	4700 2150 4700 2800
Wire Wire Line
	4100 2050 4100 2800
Connection ~ 4100 2800
Wire Wire Line
	4000 4250 4000 5550
Wire Wire Line
	4100 2800 4100 4150
Wire Wire Line
	4000 5550 8900 5550
Wire Wire Line
	8900 5550 8900 4850
Connection ~ 8900 4850
$Comp
L Device:LED D1
U 1 1 5E645FB1
P 9850 2950
F 0 "D1" H 9843 2695 50  0000 C CNN
F 1 "LED" H 9843 2786 50  0000 C CNN
F 2 "My_Misc:LED_D5.0mm_larger_pads" H 9850 2950 50  0001 C CNN
F 3 "~" H 9850 2950 50  0001 C CNN
	1    9850 2950
	-1   0    0    1   
$EndComp
$Comp
L Device:R R9
U 1 1 5E6478D8
P 9850 2550
F 0 "R9" V 9643 2550 50  0000 C CNN
F 1 "220R" V 9734 2550 50  0000 C CNN
F 2 "My_Misc:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal_larger_pads" V 9780 2550 50  0001 C CNN
F 3 "~" H 9850 2550 50  0001 C CNN
	1    9850 2550
	0    1    1    0   
$EndComp
Wire Wire Line
	6650 3200 9450 3200
Wire Wire Line
	9450 3200 9450 2950
Wire Wire Line
	9450 2950 9700 2950
Connection ~ 9450 3200
Wire Wire Line
	9450 3200 9700 3200
Wire Wire Line
	10000 2950 10250 2950
Wire Wire Line
	10250 2950 10250 2550
Wire Wire Line
	10250 2550 10000 2550
Wire Wire Line
	9700 2550 8900 2550
Wire Wire Line
	8900 2550 8900 3400
Connection ~ 8900 3400
Wire Wire Line
	4000 2700 4000 4250
Wire Wire Line
	3650 3350 3900 3350
Wire Wire Line
	3900 3350 3900 3100
Wire Wire Line
	3900 3100 5050 3100
Wire Wire Line
	3650 3450 4200 3450
Wire Wire Line
	4200 3450 4200 2800
Wire Wire Line
	4200 2800 4700 2800
Connection ~ 4700 2800
$EndSCHEMATC
