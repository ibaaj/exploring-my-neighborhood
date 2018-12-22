library(ggmap)
library(geosphere)

register_google(key = "GOOGLE KEY")


split_df <- function(data, n){
  rownames(data) <- c(1:nrow(data))
  split_list <- list()
  split_size <- nrow(data) %/% n
  for (i in 1:(n - 1)){
    split_list[[i]] <- data[(((i - 1) * split_size) + 1):(i * split_size), ]
  }
  split_list[[n]] <- data[(((n - 1) * split_size) + 1):nrow(data), ]
  split_list
}

map <- get_map(location = c(lat=48.8548825,lon=2.347492800000),maptype='satellite',zoom = 12, scale = 4, api_key = "GOOGLE KEY")
g <- ggmap(map)
df <- read.csv("all.csv")


df$distanceFromHome  <- distm(df[,3:4], c(HOME_LONGITUDE, HOME_LATITUDE), fun = distHaversine)
df <- df[order(df$distanceFromHome),]

df <- subset(df, df$distanceFromHome > 50)


n <- 50
nr <- nrow(df)

for(i in 0:49){
  j <- i + 1
  dfn <- head(df,j*ceiling(nr/n))
  print(nrow(dfn))
  g <- g + geom_point(aes(x=longitude, y=latitude), data=dfn, col="orange", alpha=0.3, size=1)
  filename <- sprintf("./img/map-%d.jpg",i)
    ggsave(file=filename,plot=g, width=20, height=20)
}

ggsave(file="map.pdf", width=20, height=20)
