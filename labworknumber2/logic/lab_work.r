data <- c(
  5.56, 3.27, 3.02, 3.47, 3.27, 3.37, 3.47, 3.47, 5.33, 5.11,
  5.33, 5.47, 5.33, 5.33, 5.47, 3.05, 5.33, 5.85, 2.68, 5.11,
  2.54, 5.43, 5.64, 1.21, 3.68, 5.43, 5.79, 2.47, 5.21, 5.47,
  4.43, 7.43, 5.47, 5.27, 5.68, 7.43, 5.47, 5.79, 5.47, 5.54,
  5.43, 7.43, 7.61, 5.47, 5.27, 7.54, 4.61, 5.54, 5.64, 5.54,
  5.64, 2.43, 3.33, 5.11, 5.33, 6.33, 6.33, 4.54, 4.64, 5.64,
  5.40, 7.68, 5.43, 1.54, 6.43, 5.37, 5.37, 5.21, 5.64, 5.64,
  5.71, 4.47, 5.21, 5.33, 2.43, 7.73, 5.43, 6.27, 5.21, 2.54,
  4.79, 3.58, 1.27, 6.33, 2.40, 5.43, 2.54, 5.54, 5.54, 2.81,
  5.39, 3.47, 5.47, 5.27, 5.58, 5.43, 5.43, 5.33, 5.61, 2.54
)

n <- length(data)
Xmin <- min(data)
Xmax <- max(data)
R <- Xmax - Xmin
H <- R / (1 + 3.322 * log10(n))   

cat("Минимальное значение:", Xmin, "\n")
cat("Максимальное значение:", Xmax, "\n")
cat("Размах варьирования R:", R, "\n")
cat("Длина интервала H:", H, "\n\n")

a1 <- Xmin - H / 2
breaks <- seq(a1, Xmax + H, by = H)
cat("Границы интервалов:\n", breaks, "\n\n")

freq_table <- table(cut(data, breaks = breaks, right = FALSE))
rel_freq <- freq_table / n
midpoints <- (head(breaks, -1) + tail(breaks, -1)) / 2

grouped_table <- data.frame(
  Интервал = levels(cut(data, breaks = breaks, right = FALSE)),
  Частота = as.numeric(freq_table),
  Относительная_частота = round(as.numeric(rel_freq), 3)
)

print(grouped_table)

output_dir <- "result"
if (!dir.exists(output_dir)) {
  dir.create(output_dir)
  cat("Создана папка:", output_dir, "\n")
}

png(file.path(output_dir, "histogram.png"), width = 800, height = 600)
hist(data, breaks = breaks, right = FALSE, col = "lightblue",
     main = "Гистограмма интервального ряда",
     xlab = "Значения признака", ylab = "Частота", border = "white")
dev.off()

png(file.path(output_dir, "frequency_polygon.png"), width = 800, height = 600)
plot(midpoints, as.numeric(freq_table), type = "b", pch = 19, col = "red",
     xlab = "Середины интервалов", ylab = "Частота",
     main = "Полигон частот")
dev.off()

png(file.path(output_dir, "relative_frequency_polygon.png"), width = 800, height = 600)
plot(midpoints, as.numeric(rel_freq), type = "b", pch = 19, col = "blue",
     xlab = "Середины интервалов", ylab = "Относительная частота",
     main = "Полигон относительных частот")
dev.off()

mean_val <- mean(data)
median_val <- median(data)
sd_val <- sd(data)

cat("\nСреднее значение:", mean_val, "\n")
cat("Медиана:", median_val, "\n")
cat("Стандартное отклонение:", sd_val, "\n")

cat("\n✅ Графики сохранены в папке:", output_dir, "\n")
