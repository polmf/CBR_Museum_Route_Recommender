library(dplyr)

artworks <- read.csv("C:/Users/lolam/Desktop/SBC_2/artworks/Artworks.txt", header = TRUE, stringsAsFactors = FALSE)
nrow(artworks)

artworks_1 <- artworks[, c("Title", "Artist", "ConstituentID", "Date", "Medium", "Dimensions", "Classification", "URL", "ImageURL")]
colnames(artworks_1)

# Ens quedem amb una sola aparicio de les obres que tenen el mateix titol
artworks_1 <- artworks_1 %>% distinct(Title, .keep_all = TRUE)
nrow(artworks_1)

unique(artworks_1$Classification)

# ens quedem només amb els que tinguin les següents classificacions (per descartar escultures, vídeos, etc)
# com la base de dades és molt gran ens ho podem permetre
artworks_2 <- subset(artworks_1, Classification %in% c("Print", "Drawing", "Painting", "Poster", "Collage", "Digital"))
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
  ) %>%
  select(-c(width_height, cm_values, Dimensions)) 

sum(is.na(artworks_3$Dim_cm2))  # Comprovar quantes files tenen NA

artworks_3 <- artworks_3 %>% filter(!is.na(Dim_cm2)) # aqui ens carreguem un munt: de moment es la manera. Intentar millorar-ho 
nrow(artworks_3)

head(artworks_3[, "Dim_cm2"]) # veie, que queda en cm quadrats
colnames(artworks_3)

# preprocessar data
artworks_subset <- artworks_3 %>%
  filter(!is.na(Date) & Date != "" & Date != "Unknown") %>%  # Eliminar files amb valors buits o NA a 'Date'
  mutate(
    # Extreure només el primer any que apareix a 'Date'
    Date = gsub(".*?(\\b\\d{4}\\b).*", "\\1", Date),
    # Comprovar que el valor extret és un any vàlid abans de convertir-lo a numèric
    Date = ifelse(grepl("^\\d{4}$", Date), as.numeric(Date), NA)
  )
nrow(artworks_subset)
table(is.na(artworks_subset$Date))  # Comprovar quantes files tenen NA a 'Date'
artworks_subset <- artworks_subset %>% filter(!is.na(Date)) # eliminarles

head(artworks_subset$Date)

#  año más antiguo y el más reciente
anio_mas_antiguo <- min(artworks_subset$Date, na.rm = TRUE)
anio_mas_reciente <- max(artworks_subset$Date, na.rm = TRUE)

# Mostrar los resultados
print(paste("El año más antiguo es:", anio_mas_antiguo))
print(paste("El año más reciente es:", anio_mas_reciente))

library(dplyr)

# añadimos la columna 'estilo' según los rangos de años definidos
artworks_final <- artworks_subset %>%
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


head(artworks_final[, c("Date", "Style")])

list_cols <- sapply(artworks_final, is.list)
list_cols

getwd()
write.csv(artworks_final, file = "artworks_final.csv", row.names = FALSE)
colnames(artworks_final)

# artworks_subset_1 te missing data, pero no es important

