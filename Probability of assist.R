# Read in Data and clean
library(readr)
library(data.table)
shot2014 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2014-15_nba_shot_log.txt", 
                                      "\t", escape_double = FALSE, trim_ws = TRUE)
shot2014 <- as.data.frame(shot2014)

shot2014$GAME_ID <- as.integer(shot2014$GAME_ID)
shot2014 <- shot2014[
  order( shot2014$GAME_ID, shot2014$PERIOD, -shot2014$GAME_CLOCK ),
  ]

shot2014$shot_count <- with(shot2014, ave(as.character(GAME_ID), GAME_ID, FUN= seq_along))

# 2015

shot2015 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2015-16_nba_shot_log.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)
shot2015 <- as.data.frame(shot2015)

shot2015$GAME_ID <- as.integer(shot2015$GAME_ID)
shot2015 <- shot2015[
  order( shot2015$GAME_ID, shot2015$PERIOD, -shot2015$GAME_CLOCK ),
  ]

shot2015$shot_count <- with(shot2015, ave(as.character(GAME_ID), GAME_ID, FUN= seq_along))


# 2016 
shot2016 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2016-17_nba_shot_log.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)
shot2016 <- as.data.frame(shot2016)

shot2016$GAME_ID <- as.integer(shot2016$GAME_ID)

shot2016 <- shot2016[
  order( shot2016$GAME_ID, shot2016$PERIOD, -shot2016$GAME_CLOCK ),
  ]

shot2016$shot_count <- with(shot2016, ave(as.character(GAME_ID), GAME_ID, FUN= seq_along))


playbyplay <- fread("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/data/Play_by_Play_New.csv") 

# Filter by year
playbyplay14 <- playbyplay[playbyplay$Season==2014,]
playbyplay14 <- playbyplay14[playbyplay14$Season_Type=="Regular",]
playbyplay14 <- playbyplay14[playbyplay14$Shot_Outcome == 1 | playbyplay14$Shot_Outcome == 0, ]
playbyplay14$shot_count <- with(playbyplay14, ave(as.character(Game_id), Game_id, FUN= seq_along))



playbyplay15 <- playbyplay[playbyplay$Season==2015,]
playbyplay15 <- playbyplay15[playbyplay15$Season_Type=="Regular",]
playbyplay15 <- playbyplay15[playbyplay15$Shot_Outcome == 1 | playbyplay15$Shot_Outcome == 0, ]
playbyplay15$shot_count <- with(playbyplay15, ave(as.character(Game_id), Game_id, FUN= seq_along))


playbyplay16 <- playbyplay[playbyplay$Season==2016,]
playbyplay16 <- playbyplay16[playbyplay16$Season_Type=="Regular",]
playbyplay16 <- playbyplay16[playbyplay16$Shot_Outcome == 1 | playbyplay16$Shot_Outcome == 0, ]
playbyplay16$shot_count <- with(playbyplay16, ave(as.character(Game_id), Game_id, FUN= seq_along))


# Merge Files

# Merge by game id and filter by period
library(dplyr)
Assist14 <- playbyplay14 %>%
  inner_join(shot2014, by= c("Game_id"="GAME_ID", "shot_count"= "shot_count"))

Assist15 <- playbyplay15 %>%
  inner_join(shot2015, by= c("Game_id"="GAME_ID", "shot_count"= "shot_count"))

Assist16 <- playbyplay16 %>%
  inner_join(shot2016, by= c("Game_id"="GAME_ID", "shot_count"= "shot_count"))


