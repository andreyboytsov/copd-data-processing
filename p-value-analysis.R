install.packages("mlogit")

library(nnet)
library(mlogit)

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

all_data$manual_Triage_1 = all_data$manual_Triage==1
all_data$manual_Triage_3 = all_data$manual_Triage==3
all_data$manual_Triage_5 = all_data$manual_Triage==5

all_data$question_Triage_1 = all_data$question_Triage==1
all_data$question_Triage_3 = all_data$question_Triage==3
all_data$question_Triage_5 = all_data$question_Triage==5

all_data$spo2_Triage_1 = all_data$spo2_Triage==1
all_data$spo2_Triage_3 = all_data$spo2_Triage==3
all_data$spo2_Triage_5 = all_data$spo2_Triage==5

all_data$pulse_Triage_1 = all_data$pulse_Triage==1
all_data$pulse_Triage_3 = all_data$pulse_Triage==3
all_data$pulse_Triage_5 = all_data$pulse_Triage==5

#sum.man.weather = summary(man.weather)
#pt(abs(sum.man.weather$coefficients / sum.man.weather$standard.errors), df=nrow(all_data)-10, lower=FALSE) 


# ================== LOGISTIC REGRESSION - Multinomial (mlogit package) =======================
manual_data = mlogit.data(all_data,choice = 'manual_Triage', shape = "wide")
question_data = mlogit.data(all_data,choice = 'question_Triage', shape = "wide")
pulse_data = mlogit.data(all_data,choice = 'pulse_Triage', shape = "wide")
spo2_data = mlogit.data(all_data,choice = 'spo2_Triage', shape = "wide")

# ================== Will be used in the article - 0h ================================

man.model <- mlogit(manual_Triage ~ 1 | temp + pressure + humidity, data = man_data)
summary(man.model)

quest.model <- mlogit(question_Triage ~ 1 | temp + pressure + humidity, data = question_data)
summary(quest.model)

pulse.model <- mlogit(pulse_Triage ~ 1 | temp + pressure + humidity, data = pulse_data)
summary(pulse.model)

spo2.model <- mlogit(spo2_Triage ~ 1 | temp + pressure + humidity, data = spo2_data)
summary(spo2.model)


# ================== Will be used in the article - 4h ================================

man_avg4h.model <- mlogit(manual_Triage ~ 1 | temp_avg4h + pressure_avg4h + humidity_avg4h, data = man_data)
summary(man_avg4h.model)

quest_avg4h.model <- mlogit(question_Triage ~ 1 | temp_avg4h + pressure_avg4h + humidity_avg4h, data = question_data)
summary(quest_avg4h.model)

pulse_avg4h.model <- mlogit(pulse_Triage ~ 1 | temp_avg4h + pressure_avg4h + humidity_avg4h, data = pulse_data)
summary(pulse_avg4h.model)

spo2_avg4h.model <- mlogit(spo2_Triage ~ 1 | temp_avg4h + pressure_avg4h + humidity_avg4h, data = spo2_data)
summary(spo2_avg4h.model)


# ================== Will be used in the article - 8h ================================

man_avg8h.model <- mlogit(manual_Triage ~ 1 | temp_avg8h + pressure_avg8h + humidity_avg8h, data = man_data)
summary(man_avg8h.model)

quest_avg8h.model <- mlogit(question_Triage ~ 1 | temp_avg8h + pressure_avg8h + humidity_avg8h, data = question_data)
summary(quest_avg8h.model)

pulse_avg8h.model <- mlogit(pulse_Triage ~ 1 | temp_avg8h + pressure_avg8h + humidity_avg8h, data = pulse_data)
summary(pulse_avg8h.model)

spo2_avg8h.model <- mlogit(spo2_Triage ~ 1 | temp_avg8h + pressure_avg8h + humidity_avg8h, data = spo2_data)
summary(spo2_avg8h.model)


# ================== Will be used in the article - 12h ================================

man_avg12h.model <- mlogit(manual_Triage ~ 1 | temp_avg12h + pressure_avg12h + humidity_avg12h, data = man_data)
summary(man_avg12h.model)

quest_avg12h.model <- mlogit(question_Triage ~ 1 | temp_avg12h + pressure_avg12h + humidity_avg12h, data = question_data)
summary(quest_avg12h.model)

pulse_avg12h.model <- mlogit(pulse_Triage ~ 1 | temp_avg12h + pressure_avg12h + humidity_avg12h, data = pulse_data)
summary(pulse_avg12h.model)

spo2_avg12h.model <- mlogit(spo2_Triage ~ 1 | temp_avg12h + pressure_avg12h + humidity_avg12h, data = spo2_data)
summary(spo2_avg12h.model)



# ================== LOGISTIC REGRESSION - Multinomial =======================
# ================== Will be used in the article - 0h ================================
man.weather <- multinom(manual_Triage ~ temp + pressure + humidity, data = all_data, na.action=na.exclude)
summary(man.weather)

quest.weather <- multinom(question_Triage ~ temp + pressure + humidity, data = all_data, na.action=na.exclude)
summary(quest.weather)

pulse.weather <- multinom(pulse_Triage ~ temp + pressure + humidity, data = all_data, na.action=na.exclude)
summary(pulse.weather)

spo2.weather <- multinom(spo2_Triage ~ temp + pressure + humidity, data = all_data, na.action=na.exclude)
summary(spo2.weather)





# ================== Will be used in the article - 4h ================================
man_avg4h.weather <- multinom(manual_Triage ~ temp_avg4h + pressure_avg4h + humidity_avg4h,
                        data = all_data, na.action=na.exclude)
summary(man_avg4h.weather)

quest_avg4h.weather <- multinom(question_Triage ~ temp_avg4h + pressure_avg4h + humidity_avg4h,
                          data = all_data, na.action=na.exclude)
summary(quest_avg4h.weather)

pulse_avg4h.weather <- multinom(pulse_Triage ~ temp_avg4h + pressure_avg4h + humidity_avg4h,
                          data = all_data, na.action=na.exclude)
summary(pulse_avg4h.weather)

spo2_avg4h.weather <- multinom(spo2_Triage ~ temp_avg4h + pressure_avg4h + humidity_avg4h,
                         data = all_data, na.action=na.exclude)
summary(spo2_avg4h.weather)



# ================== Will be used in the article - 8h ================================
man_avg8h.weather <- multinom(manual_Triage ~ temp_avg8h + pressure_avg8h + humidity_avg8h,
                        data = all_data, na.action=na.exclude)
summary(man_avg8h.weather)

quest_avg8h.weather <- multinom(question_Triage ~ temp_avg8h + pressure_avg8h + humidity_avg8h,
                          data = all_data, na.action=na.exclude)
summary(quest_avg8h.weather)

pulse_avg8h.weather <- multinom(pulse_Triage ~ temp_avg8h + pressure_avg8h + humidity_avg8h,
                          data = all_data, na.action=na.exclude)
summary(pulse_avg8h.weather)

spo2_avg8h.weather <- multinom(spo2_Triage ~ temp_avg8h + pressure_avg8h + humidity_avg8h,
                         data = all_data, na.action=na.exclude)
summary(spo2_avg8h.weather)



# ================== Will be used in the article - 12h ================================
man_avg12h.weather <- multinom(manual_Triage ~ temp_avg12h + pressure_avg12h + humidity_avg12h,
                         data = all_data, na.action=na.exclude)
summary(man_avg12h.weather)

quest_avg12h.weather <- multinom(question_Triage ~ temp_avg12h + pressure_avg12h + humidity_avg12h,
                           data = all_data, na.action=na.exclude)
summary(quest_avg12h.weather)

pulse_avg12h.weather <- multinom(pulse_Triage ~ temp_avg12h + pressure_avg12h + humidity_avg12h,
                           data = all_data, na.action=na.exclude)
summary(pulse_avg12h.weather)

spo2_avg12h.weather <- multinom(spo2_Triage ~ temp_avg12h + pressure_avg12h + humidity_avg12h,
                          data = all_data, na.action=na.exclude)
summary(spo2_avg12h.weather)







# ================== LOGISTIC REGRESSION - manual =====================
# ================== Will be used in the article - 0h ================================
man.weather.1 <- glm(manual_Triage_1 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                   family = "binomial")
summary(man.weather.1)

man.weather.3 <- glm(manual_Triage_3 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                     family = "binomial")
summary(man.weather.3)

man.weather.5 <- glm(manual_Triage_5 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                     family = "binomial")
summary(man.weather.5)


quest.weather.1 <- glm(question_Triage_1 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                     family = "binomial")
summary(quest.weather.1)

quest.weather.3 <- glm(question_Triage_3 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                     family = "binomial")
summary(quest.weather.3)

quest.weather.5 <- glm(question_Triage_5 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                     family = "binomial")
summary(quest.weather.5)



pulse.weather.1 <- glm(pulse_Triage_1 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                     family = "binomial")
summary(pulse.weather.1)

pulse.weather.3 <- glm(pulse_Triage_3 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                       family = "binomial")
summary(pulse.weather.3)

pulse.weather.5 <- glm(pulse_Triage_5 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                       family = "binomial")
summary(pulse.weather.5)



spo2.weather.1 <- glm(spo2_Triage_1 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                    family = "binomial")
summary(spo2.weather.1)

spo2.weather.3 <- glm(spo2_Triage_3 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                    family = "binomial")
summary(spo2.weather.3)

spo2.weather.5 <- glm(spo2_Triage_5 ~ temp + pressure + humidity, data = all_data, na.action=na.exclude,
                    family = "binomial")
summary(spo2.weather.5)



# ================== Will be used in the article - 4h ================================
man.weather_avg4h.1 <- glm(manual_Triage_1 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                     family = "binomial")
summary(man.weather_avg4h.1)

man.weather_avg4h.3 <- glm(manual_Triage_3 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                     family = "binomial")
summary(man.weather_avg4h.3)

man.weather_avg4h.5 <- glm(manual_Triage_5 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                     family = "binomial")
summary(man.weather_avg4h.5)


quest.weather_avg4h.1 <- glm(question_Triage_1 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                       family = "binomial")
summary(quest.weather_avg4h.1)

quest.weather_avg4h.3 <- glm(question_Triage_3 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                       family = "binomial")
summary(quest.weather_avg4h.3)

quest.weather_avg4h.5 <- glm(question_Triage_5 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                       family = "binomial")
summary(quest.weather_avg4h.5)



pulse.weather_avg4h.1 <- glm(pulse_Triage_1 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                       family = "binomial")
summary(pulse.weather_avg4h.1)

pulse.weather_avg4h.3 <- glm(pulse_Triage_3 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                       family = "binomial")
summary(pulse.weather_avg4h.3)

pulse.weather_avg4h.5 <- glm(pulse_Triage_5 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                       family = "binomial")
summary(pulse.weather_avg4h.5)



spo2.weather_avg4h.1 <- glm(spo2_Triage_1 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                      family = "binomial")
summary(spo2.weather_avg4h.1)

spo2.weather_avg4h.3 <- glm(spo2_Triage_3 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                      family = "binomial")
summary(spo2.weather_avg4h.3)

spo2.weather_avg4h.5 <- glm(spo2_Triage_5 ~ temp_avg4h + pressure_avg4h + humidity_avg4h, data = all_data, na.action=na.exclude,
                      family = "binomial")
summary(spo2.weather_avg4h.5)



# ================== Will be used in the article - 8h ================================
man.weather_avg8h.1 <- glm(manual_Triage_1 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                           family = "binomial")
summary(man.weather_avg8h.1)

man.weather_avg8h.3 <- glm(manual_Triage_3 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                           family = "binomial")
summary(man.weather_avg8h.3)

man.weather_avg8h.5 <- glm(manual_Triage_5 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                           family = "binomial")
summary(man.weather_avg8h.5)


quest.weather_avg8h.1 <- glm(question_Triage_1 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(quest.weather_avg8h.1)

quest.weather_avg8h.3 <- glm(question_Triage_3 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(quest.weather_avg8h.3)

quest.weather_avg8h.5 <- glm(question_Triage_5 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(quest.weather_avg8h.5)



pulse.weather_avg8h.1 <- glm(pulse_Triage_1 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(pulse.weather_avg8h.1)

pulse.weather_avg8h.3 <- glm(pulse_Triage_3 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(pulse.weather_avg8h.3)

pulse.weather_avg8h.5 <- glm(pulse_Triage_5 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(pulse.weather_avg8h.5)



spo2.weather_avg8h.1 <- glm(spo2_Triage_1 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                            family = "binomial")
summary(spo2.weather_avg8h.1)

spo2.weather_avg8h.3 <- glm(spo2_Triage_3 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                            family = "binomial")
summary(spo2.weather_avg8h.3)

spo2.weather_avg8h.5 <- glm(spo2_Triage_5 ~ temp_avg8h + pressure_avg8h + humidity_avg8h, data = all_data, na.action=na.exclude,
                            family = "binomial")
summary(spo2.weather_avg8h.5)




# ================== Will be used in the article - 12h ================================
man.weather_avg12h.1 <- glm(manual_Triage_1 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                           family = "binomial")
summary(man.weather_avg12h.1)

man.weather_avg12h.3 <- glm(manual_Triage_3 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                           family = "binomial")
summary(man.weather_avg12h.3)

man.weather_avg12h.5 <- glm(manual_Triage_5 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                           family = "binomial")
summary(man.weather_avg12h.5)


quest.weather_avg12h.1 <- glm(question_Triage_1 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(quest.weather_avg12h.1)

quest.weather_avg12h.3 <- glm(question_Triage_3 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(quest.weather_avg12h.3)

quest.weather_avg12h.5 <- glm(question_Triage_5 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(quest.weather_avg12h.5)



pulse.weather_avg12h.1 <- glm(pulse_Triage_1 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(pulse.weather_avg12h.1)

pulse.weather_avg12h.3 <- glm(pulse_Triage_3 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(pulse.weather_avg12h.3)

pulse.weather_avg12h.5 <- glm(pulse_Triage_5 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                             family = "binomial")
summary(pulse.weather_avg12h.5)



spo2.weather_avg12h.1 <- glm(spo2_Triage_1 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                            family = "binomial")
summary(spo2.weather_avg12h.1)

spo2.weather_avg12h.3 <- glm(spo2_Triage_3 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                            family = "binomial")
summary(spo2.weather_avg12h.3)

spo2.weather_avg12h.5 <- glm(spo2_Triage_5 ~ temp_avg12h + pressure_avg12h + humidity_avg12h, data = all_data, na.action=na.exclude,
                            family = "binomial")
summary(spo2.weather_avg12h.5)







# ================== LINEAR REGRESSION =======================
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
