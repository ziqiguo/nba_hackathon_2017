# Read in Data and clean
library(readr)
library(data.table)
shot2014 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2014-15_nba_shot_log.txt", 
                                      "\t", escape_double = FALSE, trim_ws = TRUE)
shot2014 <- as.data.frame(shot2014)

shot2014$GAME_ID <- as.integer(shot2014$GAME_ID)

shot2014$shot_count <- with(shot2014, ave(as.character(GAME_ID), GAME_ID, FUN= seq_along))

# 2015

shot2015 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2015-16_nba_shot_log.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)
shot2015 <- as.data.frame(shot2015)

shot2015$GAME_ID <- as.integer(shot2015$GAME_ID)

# 2016 
shot2016 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2016-17_nba_shot_log.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)
shot2016 <- as.data.frame(shot2016)

shot2016$GAME_ID <- as.integer(shot2016$GAME_ID)

playbyplay <- fread("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/data/Play_by_Play_New.csv") 

# Filter by year
playbyplay14 <- playbyplay[playbyplay$Season==2014,]
playbyplay14 <- playbyplay14[playbyplay14$Season_Type=="Regular",]
playbyplay14$shot <- +(grepl( "shot", playbyplay14$General_Description, ignore.case = T) )
playbyplay14 <- playbyplay14[playbyplay14$shot ==1,]
playbyplay14$shot_count <- with(playbyplay14, ave(as.character(Game_id), Game_id, FUN= seq_along))



playbyplay15 <- playbyplay[playbyplay$Season==2015,]
playbyplay15 <- playbyplay15[playbyplay15$Season_Type=="Regular",]
playbyplay15 <- playbyplay15[playbyplay15$Shot_Outcome == 1 | playbyplay15$Shot_Outcome == 0, ]


playbyplay16 <- playbyplay[playbyplay$Season==2016,]
playbyplay16 <- playbyplay16[playbyplay16$Season_Type=="Regular",]
playbyplay16 <- playbyplay16[playbyplay16$Shot_Outcome == 1 | playbyplay16$Shot_Outcome == 0, ]


# Merge Files

# Merge by game id and filter by period
library(dplyr)
Assist14 <- playbyplay14 %>%
  inner_join(shot2014, by= c("Game_id"="GAME_ID", "shot_count"= "shot_count"))

