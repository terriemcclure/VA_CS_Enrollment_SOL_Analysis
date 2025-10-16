# tmcclur-M2-2 Assignment.py
# =======================================================
# Assignment: M8.1: Final Project - R
# Name: Terrie McClure
# Email: tmcclur@gmu.edu
# GNumber: G00239649
# Course section: Analytics Big Data to Info, AIT 580, Section 011
# =======================================================
# Data Exploration Using R, SOL_CS_by_gender.csv dataset
# ===============================================

if (!require(janitor)) install.packages("janitor")
if (!require(readr)) install.packages("readr")
if (!require(ggplot2)) install.packages("ggplot2")
if (!require(scales)) install.packages("scales")
if (!require(patchwork)) install.packages("patchwork")
library(janitor)
library(dplyr)
library(stringr)
library(readr)
library(ggplot2)
library(scales)
library(patchwork)

options(width = 300) 

# =================================================
# set working directory
setwd("C:/Users/Terri/My Drive (terriemcclure@gmail.com)/Terrie/Terrie GitHub/VA_CS_Enrollment_SOL_Analysis")
getwd()

# =================================================
# ingest (read) the data into a dataframe, add a spare
SOL_CS_by_gender_orig <- read.csv("./code_output/SOL_CS_by_gender.csv", header=TRUE, sep=",", skip = 0)
SOL_CS_by_gender <- read.csv("./code_output/SOL_CS_by_gender.csv", header=TRUE, sep=",", skip = 0)

# show dataframe
# SOL_CS_by_gender
# display some of the data records
head(SOL_CS_by_gender)
tail(SOL_CS_by_gender, 8)

# =================================================

# inspect the size and other characteristics of the dataset
# in particular, what are the names of the data variables
class(SOL_CS_by_gender)
str(SOL_CS_by_gender) # brief summary of data types and values
nrow(SOL_CS_by_gender)
ncol(SOL_CS_by_gender)
dim(SOL_CS_by_gender)
names(SOL_CS_by_gender)
colnames(SOL_CS_by_gender)


# explore the data; generate some summary statistics
summary(SOL_CS_by_gender)
summary(SOL_CS_by_gender$pass_rate)

# display ONE of the data fields,
# note the syntax: dframe$colname
head(SOL_CS_by_gender$pass_rate)

# display summary stats
summary(SOL_CS_by_gender$pass_rate)
mean(SOL_CS_by_gender$pass_rate)
# remember, not too many precision digits:
round(mean(SOL_CS_by_gender$pass_rate), digits=1)

# display typical stats for numeric data field
max(SOL_CS_by_gender$pass_rate)
median(SOL_CS_by_gender$pass_rate)
round(sd(SOL_CS_by_gender$pass_rate), digits = 1)

# explore additional data visualizations
# "Tukey's 5 numbers" (Min, LowrQrtl, Median, UpprQrtl, Max)
fivenum(SOL_CS_by_gender$pass_rate)

boxplot(SOL_CS_by_gender$pass_rate, xlab="Pass Rate", ylab="%")
# compare multiple boxplots
boxplot(SOL_CS_by_gender$pass_rate ~ SOL_CS_by_gender$gender,xlab="Gender", ylab="Pass Rate %")

# Histogram
hist(SOL_CS_by_gender$pass_rate,col=(300))

# make a well-labeled visualization)
plot(SOL_CS_by_gender$CS_enrollment_rate, SOL_CS_by_gender$pass_rate,
     main="CS Enrollment Rate\nand SOL Pass Rate", xlab="CS Enrollment Rate",
     ylab="SOL Pass Rate", col="red")

# what happens when you try this?
mean(SOL_CS_by_gender$pass_rate)
# then try this
round(mean(SOL_CS_by_gender$pass_rate, na.rm = TRUE), digits = 0)

# generate stats on a [SUBSET] of the data
summary(SOL_CS_by_gender$CS_enrollment_rate[SOL_CS_by_gender$gender == 'M'])
summary(SOL_CS_by_gender$CS_enrollment_rate[SOL_CS_by_gender$gender == 'F'])

# check and test Correlation Coefficient
round(cor(SOL_CS_by_gender$CS_enrollment_rate, SOL_CS_by_gender$pass_rate), digits = 2)
cor.test(SOL_CS_by_gender$CS_enrollment_rate, SOL_CS_by_gender$pass_rate)

# lattice demo
library(lattice)  # for convenient multivariate display
histogram(~ CS_enrollment_rate | gender,
    data=SOL_CS_by_gender,
    layout=c(5,1)) # columns and rows of individual plots
# =================================================

# group by statistics (mean pass rates by year)
by_year <- SOL_CS_by_gender |>
  group_by(year) |>
  summarise(
    pass_rate = round(mean(pass_rate, na.rm = TRUE), 1),
    .groups = "drop"
  )
print(as.data.frame(by_year), row.names = FALSE)

# Line chart with points
ggplot(by_year, aes(x = year, y = pass_rate)) +
  geom_line() +
  geom_point(size = 2) +
  labs(title = "Average Pass Rate by Year",
       x = NULL,
       y = "Pass Rate (%)") +
  scale_x_continuous(breaks = by_year$year) +
  theme_minimal(base_size = 13)

# group by statistics (median pass rates by school level)
med_pass <- SOL_CS_by_gender |>
  group_by(gender) |>
  summarise(pass_rate = round(median(pass_rate, na.rm = TRUE), 1),
            .groups = "drop")
print(as.data.frame(med_pass), row.names = FALSE)

# group by statistics (median pass advanced rates by school level)
med_adv <- SOL_CS_by_gender |>
  group_by(gender) |>
  summarise(pass_advanced_rate = round(median(pass_advanced_rate, na.rm = TRUE), 1),
            .groups = "drop")
print(as.data.frame(med_adv), row.names = FALSE)

# --- Box plot: Pass Rate by Gender ---
SOL_CS_by_gender <- SOL_CS_by_gender |>
  mutate(gender = factor(gender,
                               levels = c("M", "F"),
                               ordered = TRUE))

ggplot(SOL_CS_by_gender, aes(x = gender, y = pass_rate, fill = gender)) +
  geom_boxplot(outlier.alpha = 0.4, width = 0.7) +
  labs(title = "Pass Rate by Gender",
       x = "Gender",
       y = "Pass Rate (%)") +
  coord_cartesian(ylim = c(0, 100)) +
  theme_minimal(base_size = 13) +
  theme(legend.position = "none")

# count number of EOC SOL tests by subject and STEM flag ---
tests_unique <- SOL_CS_by_gender |>
  distinct(division_name, school_name, gender)   

# count distinct schools
n_schools <- tests_unique |> distinct(division_name, school_name) |> nrow()
cat(n_schools, "\n")

# count number of tests given
n_tests   <- nrow(tests_unique)
cat(n_tests, "\n")

# group by number of tests by subject and STEM flag
by_subject_stem <- tests_unique |>
  count(gender, name = "tests") |>
  arrange(gender)

# number of EOC SOL tests given by subject and STEM/Not STEM
print(as.data.frame(by_subject_stem), row.names = FALSE)

# Bar chart: STEM vs non-STEM counts (based on unique tests)
by_stem <- tests_unique |>
  count(gender, name = "tests") |>
  mutate(pct = tests / sum(tests))

ggplot(by_stem, aes(x = as.factor(gender), y = tests, fill = as.factor(gender))) +
  geom_col(width = 0.7) +
  geom_text(aes(label = percent(pct, accuracy = 0.1)),
            vjust = -0.6, size = 4) +
  labs(title = "Count of Tests Given by STEM/NOT STEM",
       x = "STEM Flag", y = "Number of Tests Given") +
  theme_minimal(base_size = 13) +
  theme(legend.position = "none") +
  expand_limits(y = max(by_stem$tests) * 1.1)

# --- top row: histograms ---
p_hist_rate <- ggplot(SOL_CS_by_gender, aes(x = pass_rate)) +
  geom_histogram(binwidth = 10, boundary = 0, closed = "left", color = "white") +
  labs(title = "Pass Rate Histogram", y = "Frequency", x = NULL) +
  coord_cartesian(xlim = c(0, 100)) +
  theme_minimal(base_size = 13)

p_hist_adv <- ggplot(SOL_CS_by_gender, aes(x = pass_advanced_rate)) +
  geom_histogram(binwidth = 10, boundary = 0, closed = "left", color = "white") +
  labs(title = "Pass Advanced Histogram", y = "Frequency", x = NULL) +
  coord_cartesian(xlim = c(0, 100)) +
  theme_minimal(base_size = 13)

# --- bottom row: boxplots ---
p_box_rate <- ggplot(SOL_CS_by_gender, aes(x = "pass_rate", y = pass_rate)) +
  geom_boxplot(outlier.alpha = 0.6) +
  labs(title = "Pass Rate Boxplot", x = NULL, y = NULL) +
  coord_cartesian(ylim = c(0, 100)) +
  theme_minimal(base_size = 13)

p_box_adv <- ggplot(SOL_CS_by_gender, aes(x = "pass_advanced_rate", y = pass_advanced_rate)) +
  geom_boxplot(outlier.alpha = 0.6) +
  labs(title = "Pass Advanced Boxplot", x = NULL, y = NULL) +
  coord_cartesian(ylim = c(0, 100)) +
  theme_minimal(base_size = 13)

# arrange 2 × 2
(p_hist_rate | p_hist_adv) /
  (p_box_rate  | p_box_adv)


# scatter plot of cs enrollment rate vs pass rate
ggplot(SOL_CS_by_gender, aes(x = CS_enrollment_rate, y = pass_rate)) +
  geom_point(alpha = 0.25, size = 0.3) +          # many points → use transparency
  geom_smooth(method = "lm", se = FALSE, color = "red", linewidth = 1) +
  labs(
    title = "CS Enrollment Rate vs Pass Rate",
    x = "CS Enrollment Rate (%)",
    y = "Pass Rate (%)"
  ) +
  coord_cartesian(xlim = c(0, 100), ylim = c(-25, 100)) +
  theme_minimal(base_size = 13)

CS_by_gender <- SOL_CS_by_gender |>
  group_by(gender) |>
  summarise(
    avg_cs_enrollment_rate = weighted.mean(CS_enrollment_rate, total_count, na.rm = TRUE),
    avg_pass_rate = weighted.mean(pass_rate, total_count, na.rm = TRUE),
    avg_pass_rate_stem = weighted.mean(pass_rate_stem, total_count, na.rm = TRUE),
    avg_pass_rate_non_stem = weighted.mean(pass_rate_non_stem, total_count, na.rm = TRUE)
  )
ggplot(CS_by_gender, aes(x = gender, y = avg_cs_enrollment_rate, fill = gender)) +
  geom_col(width = 0.6) +
  geom_text(aes(label = round(avg_cs_enrollment_rate, 1)),
            vjust = -0.5, size = 6, color = "gray20") +
  scale_fill_manual(values = c("F" = "pink", "M" = "skyblue")) +
  labs(
    title = "Average Computer Science Enrollment Rates by Gender",
    subtitle = "Virginia Public High Schools, 2021–2022",
    x = NULL,
    y = "CS Enrollment Rate (%)"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5),
    axis.text = element_text(color = "gray20")
  )

ggplot(CS_by_gender, aes(x = gender, y = avg_cs_enrollment_rate, fill = gender)) +
  geom_col(width = 0.6) +
  geom_text(aes(label = round(avg_cs_enrollment_rate, 1)),
            vjust = -0.3, size = 6, fontface = "bold", color = "gray20") +
  scale_fill_manual(values = c("F" = "pink", "M" = "skyblue")) +
  labs(
    title = "Average Computer Science Enrollment Rates by Gender",
    subtitle = "Virginia Public High Schools, 2021–2022",
    x = "Gender",
    y = "CS Enrollment Rate (%)"
  ) +
  coord_cartesian(
    ylim = c(0, max(CS_by_gender$avg_cs_enrollment_rate) * 1.15),
    clip = "off"             # ⬅ prevents cutting off labels or axes
  ) +
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5),
    axis.text = element_text(color = "gray20"),
    plot.margin = margin(t = 10, r = 20, b = 50, l = 30)   # more breathing room
  )
