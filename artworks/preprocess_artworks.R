library(dplyr)

artworks <- read.csv("C:/Users/lolam/Desktop/SBC_2/artworks/Artworks.txt", header = TRUE, stringsAsFactors = FALSE)
nrow(artworks)

artworks_1 <- artworks[, c("Title", "Artist", "ConstituentID", "Date", "Medium", "Dimensions", "Classification", "URL", "ImageURL")]
colnames(artworks_1)

# Ens quedem amb una sola aparicio dels que tenen el mateix titol
artworks_1 <- artworks_1 %>% distinct(Title, .keep_all = TRUE)


unique(artworks_1$Classification)
artworks_2 <- subset(artworks_1, Classification %in% c("Print", "Drawing", "Graphic Design", "Painting", "Poster", "Collage", "Digital", "Moving Image"))
nrow(artworks_2)

# PROBLEMA: moltes es queden en NA
artworks_3 <- artworks_2 %>%
  mutate(
    cm_values = gsub(".*\\((.*) cm\\).*", "\\1", Dimensions),
    width_height = strsplit(cm_values, " x "),
    Dim_cm2 = sapply(width_height, function(x) {
      if (length(x) == 2) {
        as.numeric(x[1]) * as.numeric(x[2])
      } else {
        NA
      }
    })
  )

artworks_3 <- artworks_3 %>% select(-c(width_height, cm_values, Dimensions))

head(artworks_3[, c("Dim_cm2")])
nrow(artworks_3)

# Asegurarnos de que 'artworks_subset' sea un data frame
if (!is.data.frame(artworks_3)) {
  artworks_3 <- data.frame(artworks_3, stringsAsFactors = FALSE)
}

colnames(artworks_3)

# Limpiar la columna 'Date' para extraer solo el primer año presente y convertir a numérico si es posible
artworks_subset <- artworks_3 %>%
  filter(!is.na(Date) & Date != "") %>%  # Eliminar filas con valores NA o vacíos en Date
  mutate(
    Date = gsub(".*?(\\b\\d{4}\\b).*", "\\1", Date),  # Extraer el primer año que aparece en Date
    Date = ifelse(grepl("^\\d{4}$", Date), as.numeric(Date), NA)  # Convertir a numérico si el valor es válido
  )

# Verificar los resultados
head(artworks_subset$Date)

# Extraer el año más antiguo y el más reciente
anio_mas_antiguo <- min(artworks_subset$Date, na.rm = TRUE)
anio_mas_reciente <- max(artworks_subset$Date, na.rm = TRUE)

# Mostrar los resultados
print(paste("El año más antiguo es:", anio_mas_antiguo))
print(paste("El año más reciente es:", anio_mas_reciente))


library(dplyr)

# Añadir la columna 'estilo' según los rangos de años definidos
artworks_subset_1 <- artworks_subset %>%
  mutate(
    Style = case_when(
      Date >= 1800 & Date < 1850 ~ "Romanticismo",
      Date >= 1850 & Date < 1880 ~ "Realismo",
      Date >= 1880 & Date < 1905 ~ "Impresionismo",
      Date >= 1905 & Date < 1920 ~ "Cubismo",
      Date >= 1920 & Date < 1940 ~ "Surrealismo",
      Date >= 1940 & Date < 1960 ~ "Expresionismo Abstracto",
      Date >= 1960 & Date < 1980 ~ "Pop Art",
      Date >= 1980 & Date < 2000 ~ "Postmodernismo",
      Date >= 2000 & Date <= 2024 ~ "Arte Contemporáneo",
      TRUE ~ NA_character_  # Asignar NA a cualquier valor que no entre en los rangos especificados
    )
  )

# Verificar los primeros resultados
head(artworks_subset_1[, c("Date", "Style")])

list_cols <- sapply(artworks_subset_1, is.list)
list_cols

# Suponiendo que 'final_data' es tu DataFrame al final del script
getwd()
write.csv(artworks_subset_1, file = "artworks_subset.csv", row.names = FALSE)





