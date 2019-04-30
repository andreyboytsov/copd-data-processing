# all_data = read.csv("./Basel/Patients_and_Weather_w_history.csv")
all_data = read.csv("./data_generated/Patients_and_Weather_extended.csv")
all_data$tempCelsius <- all_data$temp - 273.15

interesting_columns_patient = c("SO2", "Pulse", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "CQ1", "CQ2",
                                "CQ3", "CQ4", "CQ5", "CQ6", "CQ7", "CQ8",
                                "question_Triage", "pulse_Triage", "spo2_Triage", "manual_Triage",
                                "SpO2ReferenceValue", "PulseReferenceValue",
                                "SpO2RedLimitVariation", "SpO2YellowLimitVariation",
                                "PulseRedLimitUpper", "PulseRedLimitLower", "PulseRedLimitVariation",
                                "PulseYellowLimitVariation")
interesting_columns_weather = c("temp", "pressure",
                                "humidity", "wind_speed", "wind_deg", "rain_1h", "rain_3h", "rain_24h",
                                "rain_today", "snow_1h", "snow_3h", "snow_24h", "snow_today",
                                "clouds_all")

# ================== Will be used in the article - 0h ================================
man.weather <- lm(manual_Triage ~ temp + pressure + humidity, data = all_data, na.action=na.exclude)
summary(man.weather)

quest.weather <- lm(question_Triage ~ temp + pressure + humidity, data = all_data, na.action=na.exclude)
summary(quest.weather)

pulse.weather <- lm(pulse_Triage ~ temp + pressure + humidity, data = all_data, na.action=na.exclude)
summary(pulse.weather)

spo2.weather <- lm(spo2_Triage ~ temp + pressure + humidity, data = all_data, na.action=na.exclude)
summary(spo2.weather)





# ================== Will be used in the article - 4h ================================
man_avg4h.weather <- lm(manual_Triage ~ temp_avg4h + pressure_avg4h + humidity_avg4h,
                  data = all_data, na.action=na.exclude)
summary(man_avg4h.weather)

quest_avg4h.weather <- lm(question_Triage ~ temp_avg4h + pressure_avg4h + humidity_avg4h,
                          data = all_data, na.action=na.exclude)
summary(quest_avg4h.weather)

pulse_avg4h.weather <- lm(pulse_Triage ~ temp_avg4h + pressure_avg4h + humidity_avg4h,
                          data = all_data, na.action=na.exclude)
summary(pulse_avg4h.weather)

spo2_avg4h.weather <- lm(spo2_Triage ~ temp_avg4h + pressure_avg4h + humidity_avg4h,
                         data = all_data, na.action=na.exclude)
summary(spo2_avg4h.weather)



# ================== Will be used in the article - 8h ================================
man_avg8h.weather <- lm(manual_Triage ~ temp_avg8h + pressure_avg8h + humidity_avg8h,
                        data = all_data, na.action=na.exclude)
summary(man_avg8h.weather)

quest_avg8h.weather <- lm(question_Triage ~ temp_avg8h + pressure_avg8h + humidity_avg8h,
                          data = all_data, na.action=na.exclude)
summary(quest_avg8h.weather)

pulse_avg8h.weather <- lm(pulse_Triage ~ temp_avg8h + pressure_avg8h + humidity_avg8h,
                          data = all_data, na.action=na.exclude)
summary(pulse_avg8h.weather)

spo2_avg8h.weather <- lm(spo2_Triage ~ temp_avg8h + pressure_avg8h + humidity_avg8h,
                         data = all_data, na.action=na.exclude)
summary(spo2_avg8h.weather)



# ================== Will be used in the article - 12h ================================
man_avg12h.weather <- lm(manual_Triage ~ temp_avg12h + pressure_avg12h + humidity_avg12h,
                         data = all_data, na.action=na.exclude)
summary(man_avg12h.weather)

quest_avg12h.weather <- lm(question_Triage ~ temp_avg12h + pressure_avg12h + humidity_avg12h,
                           data = all_data, na.action=na.exclude)
summary(quest_avg12h.weather)

pulse_avg12h.weather <- lm(pulse_Triage ~ temp_avg12h + pressure_avg12h + humidity_avg12h,
                           data = all_data, na.action=na.exclude)
summary(pulse_avg12h.weather)

spo2_avg12h.weather <- lm(spo2_Triage ~ temp_avg12h + pressure_avg12h + humidity_avg12h,
                          data = all_data, na.action=na.exclude)
summary(spo2_avg12h.weather)





# =================== MANUAL TRIAGE ==============================================
man.hist <- lm(manual_Triage ~ manual_Triage_1 + manual_Triage_2 + manual_Triage_3 + manual_Triage_4,
               data = all_data, na.action=na.exclude)
summary(man.hist)

man.hist.weather <- lm(manual_Triage ~ manual_Triage_1 + manual_Triage_2 + manual_Triage_3 + manual_Triage_4+
                    temp + pressure + humidity + wind_speed,
               data = all_data, na.action=na.exclude)
summary(man.hist.weather)




# =================== QUESTION TRIAGE ==============================================
quest.hist <- lm(question_Triage ~ question_Triage_1 + question_Triage_2 + question_Triage_3 + question_Triage_4,
               data = all_data, na.action=na.exclude)
summary(quest.hist)

quest.hist.weather <- lm(question_Triage ~ question_Triage_1 + question_Triage_2 + question_Triage_3 + question_Triage_4+
                         temp + pressure + humidity + wind_speed,
                       data = all_data, na.action=na.exclude)
summary(quest.hist.weather)

quest.weather <- lm(question_Triage ~ temp + pressure + humidity + wind_speed,
                  data = all_data, na.action=na.exclude)
summary(quest.weather)




# =================== PULSE TRIAGE ==============================================
spo2.hist <- lm(pulse_Triage ~ pulse_Triage_1 + pulse_Triage_2 + pulse_Triage_3 + pulse_Triage_4,
               data = all_data, na.action=na.exclude)
summary(spo2.hist)

spo2.hist.weather <- lm(pulse_Triage ~ pulse_Triage_1 + pulse_Triage_2 + pulse_Triage_3 + pulse_Triage_4+
                         temp * pressure * humidity + wind_speed,
                       data = all_data, na.action=na.exclude)
summary(spo2.hist.weather)

spo2.weather <- lm(pulse_Triage ~ temp + pressure + humidity + wind_speed,
                  data = all_data, na.action=na.exclude)
summary(spo2.weather)




# =================== SPO2 TRIAGE ==============================================
spo2.hist <- lm(spo2_Triage ~ spo2_Triage_1 + spo2_Triage_2 + spo2_Triage_3 + spo2_Triage_4,
               data = all_data, na.action=na.exclude)
summary(spo2.hist)

spo2.hist.weather <- lm(spo2_Triage ~ spo2_Triage_1 + spo2_Triage_2 + spo2_Triage_3 + spo2_Triage_4+
                         temp + pressure + humidity + wind_speed,
                       data = all_data, na.action=na.exclude)
summary(spo2.hist.weather)

spo2.weather <- lm(spo2_Triage ~ temp + pressure + humidity + wind_speed,
                  data = all_data, na.action=na.exclude)
summary(spo2.weather)


install.packages("tidyverse", dependencies = TRUE)
library("ggplot2")
ggplot(all_data[!is.na(all_data$manual_Triage),], aes(x=manual_Triage, y=tempCelsius)) + 
  geom_point(color='#2980B9', size = 4) + 
  geom_smooth(method=lm, color='#2C3E50')




# Well, the weather does not influence as much as history.
# If history is taken into account, the weather lose significance.

# Perhaps, we can write up as is.
install.packages("corrplot")
library(corrplot)

spo2.corr <- cor(all_data[c("spo2_Triage_1","spo2_Triage_2","spo2_Triage_3",
                            "temp","pressure","humidity","wind_speed")], use = "pairwise.complete.obs")
corrplot(spo2.corr, method="circle")


pulse.corr <- cor(all_data[c("pulse_Triage_1","pulse_Triage_2","pulse_Triage_3",
                            "temp","pressure","humidity","wind_speed")], use = "pairwise.complete.obs")
corrplot(pulse.corr, method="circle")


quest.corr <- cor(all_data[c("question_Triage_1","question_Triage_2","question_Triage_3",
                             "temp","pressure","humidity","wind_speed")], use = "pairwise.complete.obs")
corrplot(quest.corr, method="circle")

man.corr <- cor(all_data[c("manual_Triage_1","manual_Triage_2","manual_Triage_3",
                             "temp","pressure","humidity","wind_speed")], use = "pairwise.complete.obs")
corrplot(man.corr, method="circle")




# Temperature, pressure, humidity - everything.
