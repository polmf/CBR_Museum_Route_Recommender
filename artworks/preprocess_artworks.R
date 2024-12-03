library(dplyr)

artworks <- read.csv("C:/Users/lolam/Desktop/SBC_2/artworks/Artworks.txt", header = TRUE, stringsAsFactors = FALSE)
nrow(artworks)

artworks_1 <- artworks[, c("Title", "Artist", "ConstituentID", "Date", "Medium", "Dimensions", "Classification", "URL", "ImageURL")]
colnames(artworks_1)

unique(artworks_1$Classification)
artworks_2 <- subset(artworks_1, Classification %in% c("Print", "Drawing", "Graphic Design", "Painting", "Poster", "Collage", "Digital", "Moving Image"))
nrow(artworks_2)

artworks_3 <- artworks_2 %>%
  mutate(
    cm_values = gsub(".*\\((.*) cm\\).*", "\\1", Dimensions),
    width_height = strsplit(cm_values, " x "),
    dim_cm2 = sapply(width_height, function(x) {
      if (length(x) == 2) {
        as.numeric(x[1]) * as.numeric(x[2])
      } else {
        NA
      }
    })
  )

head(artworks_3[, c("dim_cm2")])
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




