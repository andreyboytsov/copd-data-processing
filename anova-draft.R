all_data = read.csv("./Basel/Patients_and_Weather.csv")
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

all_data$snow_1h[is.na(all_data$snow_1h)] <- 0
all_data$rain_1h[is.na(all_data$rain_1h)] <- 0
all_data$snow_3h[is.na(all_data$snow_3h)] <- 0
all_data$rain_3h[is.na(all_data$rain_3h)] <- 0
#all_data$snow_24h[is.na(all_data$snow_24h)] <- 0
#all_data$rain_24h[is.na(all_data$rain_24h)] <- 0

# + snow_24h + rain_24h

all_data$manual_Triage_factor <- as.factor(all_data$manual_Triage)

all_data.aov <- aov(manual_Triage ~ temp + pressure + humidity + wind_speed + snow_1h + snow_3h  + clouds_all
                    + wind_deg + rain_1h + rain_3h + weather_main + weather_description, data = all_data, na.action=na.exclude)
summary(all_data.aov)

require(ggplot2)

ggplot(all_data[!is.na(all_data$manual_Triage),], aes(x = manual_Triage, y = temp, group=manual_Triage)) +
  geom_boxplot(fill = "grey80", colour = "blue") + scale_x_discrete()

ggplot(all_data[!is.na(all_data$manual_Triage),], aes(x = manual_Triage, y = rain_3h, group=manual_Triage)) +
  geom_boxplot(fill = "grey80", colour = "blue") + scale_x_discrete()


all_data.lm <- lm(manual_Triage ~ temp + pressure + humidity + wind_speed + snow_1h + snow_3h+ clouds_all
                  + wind_deg + rain_1h + rain_3h + weather_main + weather_description, data = all_data, na.action=na.exclude)
summary(all_data.lm)


all_data.man <- manova(temp + pressure + humidity + wind_speed + snow_1h + snow_3h+ clouds_all
                  + wind_deg + rain_1h + rain_3h + weather_main + weather_description ~ manual_Triage, data = all_data, na.action=na.exclude)

all_data.aov_reverse <- aov(temp ~ manual_Triage, data = all_data, na.action=na.exclude)
summary(all_data.aov_reverse)

all_data.aov_reverse_factor <- aov(temp ~ manual_Triage_factor, data = all_data, na.action=na.exclude)
summary(all_data.aov_reverse_factor)
