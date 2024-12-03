artworks <- read.csv("C:/Users/lolam/Desktop/Artworks.txt", header = TRUE, stringsAsFactors = FALSE)
nrow(artworks)

artworks_subset <- artworks[, c("Title", "Artist", "ConstituentID", "Date", "Medium", "Dimensions", "Classification", "URL", "ImageURL")]
colnames(artworks_subset)

unique(artworks_subset$Classification)
filtered_artworks <- subset(artworks_subset, Classification %in% c("Print", "Drawing", "Graphic Design", "Painting", "Poster", "Collage", "Digital", "Moving Image"))
nrow(filtered_artworks)


library(dplyr)

artworks_with_area <- artworks_subset %>%
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

head(artworks_with_area[, c("dim_cm2")])

artworks_subset_2 <- artworks_with_area[, c("Dimensions")]

