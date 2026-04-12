library(dplyr)
library(ggplot2)
library(forcats)
library(psych)
library(corrplot)

raw_data <- read_excel("Downloads/data_full.xlsx")
View(raw_data)

data <- raw_data %>%
  mutate(
    # --- Восприятие искусства (1–4)
    dance_art_num = as.numeric(factor(dance_art,
                                      levels = c(
                                        "Полностью не согласен:а",
                                        "Скорее не согласен:а",
                                        "Скорее согласен:а",
                                        "Полностью согласен:а"
                                      )
    )),
    
    # --- Восприятие спорта (1–4)
    dance_sport_num = as.numeric(factor(dance_sport,
                                        levels = c(
                                          "Полностью не согласен:а",
                                          "Скорее не согласен:а",
                                          "Скорее согласен:а",
                                          "Полностью согласен:а"
                                        )
    )),
    
    # --- Уровень знакомства (1–3)
    know_d_num = as.numeric(factor(know_d,
                                   levels = c(
                                     "Что-то слышал:а",
                                     "Имею общее представление",
                                     "Хорошо знаком:а"
                                   )
    )),
    
    # --- Опыт (0/1)
    exp_bin = ifelse(exp == "Не имею личного опыта", 0, 1)
  ) %>%
  filter(complete.cases(dance_art_num, dance_sport_num, know_d_num))


# Распределение
table(data$dance_sport)
prop.table(table(data$dance_sport))

View(table(data$dance_art))
View(prop.table(table(data$dance_art)))

table(data$exp)
prop.table(table(data$exp))


ggplot(data, aes(x = dance_sport)) +
  geom_bar() +
  labs(title = "Восприятие бальных танцев как спорта",
       x = "Ответ",
       y = "Количество") +
  theme_minimal()




ggplot(data, aes(x = dance_art)) +
  geom_bar() +
  labs(title = "Восприятие бальных танцев как искусства",
       x = "Ответ",
       y = "Количество") +
  theme_minimal()


ggplot(data, aes(x = factor(exp_bin), fill = dance_sport)) +
  geom_bar(position = "fill") +
  labs(title = "Связь опыта и восприятия танцев как спорта",
       x = "Опыт (0 = нет, 1 = есть)",
       y = "Доля",
       fill = "Ответ") +
  theme_minimal()

ggplot(data, aes(x = factor(know_d_num), y = dance_sport_num)) +
  geom_boxplot() +
  labs(title = "Знание и восприятие танцев как спорта",
       x = "Уровень знакомства",
       y = "Оценка (спорт)") +
  theme_minimal()

ggplot(data, aes(x = dance_sport_num, y = dance_art_num)) +
  geom_jitter(width = 0.2, height = 0.2, alpha = 0.3) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(title = "Связь восприятия спорта и искусства",
       x = "Спорт",
       y = "Искусство") +
  theme_minimal()

cor.test(data$dance_sport_num, data$know_d_num, method = "spearman")
cor.test(data$dance_sport_num, data$exp_bin, method = "spearman")
cor.test(data$dance_art_num, data$exp_bin, method = "spearman")
cor.test(data$dance_art_num, data$dance_sport_num, method = "spearman")

table(data$exp, data$dance_sport)
prop.table(table(data$exp, data$dance_sport), 1)

# АНАЛИЗ ВЛИЯНИЯ ИСТОЧНИКОВ ИНФОРМАЦИИ (H3)
# Только для респондентов без личного опыта (exp == "Не имею личного опыта")

# 1. Создаём подвыборку
data_no_exp <- subset(raw_data, exp == "Не имею личного опыта")

# Проверим размер подвыборки
cat("Размер подвыборки (нет опыта):", nrow(data_no_exp), "\n")

# 2. Создаём бинарные переменные для источников (1 = выбрал, 0 = не выбрал)
#    В исходных данных, если респондент выбрал источник, в соответствующей колонке стоит текст (например, "Телевидение")
#    Если не выбрал – NA. Поэтому:
data_no_exp$tv_bin <- ifelse(!is.na(data_no_exp$know_tv), 1, 0)
data_no_exp$rs_bin <- ifelse(!is.na(data_no_exp$know_rs), 1, 0)
data_no_exp$film_bin <- ifelse(!is.na(data_no_exp$know_film), 1, 0)
data_no_exp$friends_bin <- ifelse(!is.na(data_no_exp$know_friends), 1, 0)
data_no_exp$school_bin <- ifelse(!is.na(data_no_exp$know_school), 1, 0)
data_no_exp$other_bin <- ifelse(!is.na(data_no_exp$know_other), 1, 0)

# 3. Функция для проверки связи с восприятием спорта (dance_sport)
test_source_sport <- function(source_bin, source_name) {
  cat("\n========================================\n")
  cat("Источник:", source_name, "\n")
  cat("Таблица сопряжённости (источник × dance_sport):\n")
  tab <- table(source_bin, data_no_exp$dance_sport)
  print(tab)
  # Используем тест хи-квадрат с симуляцией p-value (из-за малых ожидаемых частот)
  test <- chisq.test(tab, simulate.p.value = TRUE, B = 10000)
  cat("\nРезультаты теста:\n")
  print(test)
  cat("========================================\n")
}

# 4. Функция для проверки связи с восприятием искусства (dance_art)
test_source_art <- function(source_bin, source_name) {
  cat("\n========================================\n")
  cat("Источник:", source_name, "\n")
  cat("Таблица сопряжённости (источник × dance_art):\n")
  tab <- table(source_bin, data_no_exp$dance_art)
  print(tab)
  test <- chisq.test(tab, simulate.p.value = TRUE, B = 10000)
  cat("\nРезультаты теста:\n")
  print(test)
  cat("========================================\n")
}

# 5. Запускаем тесты для каждого источника (для dance_sport)
test_source_sport(data_no_exp$tv_bin, "Телевидение")
test_source_sport(data_no_exp$rs_bin, "Социальные сети")
test_source_sport(data_no_exp$film_bin, "Фильмы/шоу")
test_source_sport(data_no_exp$friends_bin, "Знакомые")
test_source_sport(data_no_exp$school_bin, "Общественные/школьные мероприятия")
test_source_sport(data_no_exp$other_bin, "Другое")

# 6. Запускаем тесты для каждого источника (для dance_art)
test_source_art(data_no_exp$tv_bin, "Телевидение")
test_source_art(data_no_exp$rs_bin, "Социальные сети")
test_source_art(data_no_exp$film_bin, "Фильмы/шоу")
test_source_art(data_no_exp$friends_bin, "Знакомые")
test_source_art(data_no_exp$school_bin, "Общественные/школьные мероприятия")
test_source_art(data_no_exp$other_bin, "Другое")

# 7. Дополнительно: описание распределения ответов среди тех, кто выбрал каждый источник
for (src in c("tv_bin", "rs_bin", "film_bin", "friends_bin", "school_bin", "other_bin")) {
  name <- switch(src,
                 tv_bin = "Телевидение",
                 rs_bin = "Социальные сети",
                 film_bin = "Фильмы/шоу",
                 friends_bin = "Знакомые",
                 school_bin = "Общественные/школьные",
                 other_bin = "Другое")
  cat("\n", name, ":\n")
  # Только те, кто выбрал источник
  selected <- data_no_exp[data_no_exp[[src]] == 1, ]
  if(nrow(selected) > 0) {
    cat("  Количество выбравших:", nrow(selected), "\n")
    cat("  Распределение dance_sport:\n")
    print(prop.table(table(selected$dance_sport)))
    cat("  Распределение dance_art:\n")
    print(prop.table(table(selected$dance_art)))
  } else {
    cat("  Нет респондентов, выбравших этот источник\n")
  }
}



for (src in c("tv_bin", "rs_bin", "film_bin", "friends_bin", "school_bin", "other_bin")) {
  name <- switch(src,
                 tv_bin = "Телевидение",
                 rs_bin = "Социальные сети",
                 film_bin = "Фильмы/шоу",
                 friends_bin = "Знакомые",
                 school_bin = "Общественные/школьные",
                 other_bin = "Другое")
  
  selected <- data_no_exp[data_no_exp[[src]] == 1, ]
  if(nrow(selected) > 0) {
    # --- Таблица для dance_sport (спорт) ---
    tab_sport <- prop.table(table(selected$dance_sport))
    sport_line <- paste0(
      sprintf("  %-18s [СПОРТ]     | N=%2d | ", name, nrow(selected)),
      paste(sprintf("%s: %5.1f%%", names(tab_sport), tab_sport*100), collapse = "; ")
    )
    cat(sport_line, "\n")
    
    # --- Таблица для dance_art (искусство) ---
    tab_art <- prop.table(table(selected$dance_art))
    art_line <- paste0(
      sprintf("  %-18s [ИСКУССТВО] | N=%2d | ", name, nrow(selected)),
      paste(sprintf("%s: %5.1f%%", names(tab_art), tab_art*100), collapse = "; ")
    )
    cat(art_line, "\n")
    cat("\n")   # пустая строка между источниками
  } else {
    cat(sprintf("  %-18s | нет респондентов\n", name))
  }
}
