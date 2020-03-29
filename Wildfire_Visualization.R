library(readr)

ca_fires <- read_csv("C:/Users/13604/BDBI-Datathon-CA-Wildfire-Predictive-Analysis/axios-calfire-wildfire-data.csv")

head(ca_fires)

library(lubridate)
library(dplyr)


ca_fires <- ca_fires %>%  mutate(start = as.Date(start, "%m-%d-%Y"), end = as.Date(end, "%m-%d-%Y"))

ca_fires <- ca_fires %>%  mutate(Month = month(start, label = TRUE),
                                 Year = year(start))

ca_fires <- ca_fires %>%  mutate(duration = end - start)


ca_fires <- ca_fires %>%  mutate(acres_cumulative = cumsum(acres))

group_by(ca_fires$Year,ca_fires$acres, sum)

library(ggplot2)

ggplot(data = ca_fires) +
  aes(x = acres) +
  geom_histogram(bins  = 30) +
  theme_classic() +
  scale_x_continuous(labels = scales::comma)


ca_fires %>%  filter(duration < 0)

ca_fires <- ca_fires %>%
  filter(duration >0)

## duration
ggplot(data = ca_fires) +
  aes(x = duration) +
  geom_histogram(bins  = 30) +
  theme_classic() +
  scale_x_continuous(labels = scales::comma)


month_summary <- ca_fires %>%
  group_by(Month) %>%
  summarize(fires = n())

ggplot(data = month_summary) +
  aes(x = Month, y = fires) +
  geom_bar(stat = "identity") +
  theme_classic() +
  scale_y_continuous(labels = scales::comma)


month_year_summary <- ca_fires %>%
  group_by(Month, Year) %>%
  summarize(fires = n())
ggplot(data = month_year_summary) +
  aes(x = Month, y = fires) +
  geom_boxplot() +
  theme_classic() +
  scale_y_continuous(labels = scales::comma)


ca_fires %>%
  ggplot() +
  aes(x = start, y = acres_cumulative) +
  geom_line() +
  theme_classic() +
  scale_y_continuous(labels = scales::comma) +
  ylab("Acres Burned (cumulative)") +
  xlab("date") +
  ggtitle("Cumulative Acres Burned Since 2000")

ca_fires
