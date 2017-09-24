install.packages("pacman")
library(pacman)
pacman::p_load(dplyr, readr, data.table, car, glmnet, ROCR)

# Read in Data and clean ---------

# 2014 ---------
shot2014 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2014-15_nba_shot_log.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)

shot2014 <- as.data.frame(shot2014)

shot2014$SV_PLAYER_ID <- as.factor(shot2014$SV_PLAYER_ID)

shot2014$GAME_ID <- as.integer(shot2014$GAME_ID)

# Repeat for 2015 ----------

shot2015 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2015-16_nba_shot_log.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)

shot2015 <- as.data.frame(shot2015)

shot2015$SV_PLAYER_ID <- as.factor(shot2015$SV_PLAYER_ID)

shot2015$GAME_ID <- as.integer(shot2015$GAME_ID)

# Repeat for 2016 ---------

shot2016 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2016-17_nba_shot_log.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)

shot2016 <- as.data.frame(shot2016)

shot2016$SV_PLAYER_ID <- as.factor(shot2016$SV_PLAYER_ID)

shot2016$GAME_ID <- as.integer(shot2016$GAME_ID)

# Player_Map
Player_Map <- read.csv("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/data/Player_Map.csv")

Player_Map$SV_Player_id <- as.factor(Player_Map$SV_Player_id)

# Count shots

Shots2014<- inner_join(shot2014, Player_Map, by = c("SV_PLAYER_ID" = "SV_Player_id"))

Shots2014$Player_shots <- with(Shots2014, ave(as.character(GAME_ID), SV_PLAYER_ID , FUN= seq_along))

SD14 <- aggregate(PTS ~ SV_PLAYER_ID, Shots2014, sd)
colnames(SD14) <- c("SV_PLAYER_ID", "SD14")
SD14$SD14 <- SD14$SD14/2
Points14 <- aggregate(PTS ~ GAME_ID + SV_PLAYER_ID, Shots2014, sum)
Max14 <- aggregate(Player_shots ~ SV_PLAYER_ID + GAME_ID, Shots2014, max)

Points14 <- Points14[order(Points14$GAME_ID, Points14$SV_PLAYER_ID),]
Max14 <- Max14[order(Max14$GAME_ID, Max14$SV_PLAYER_ID),]

Shots.Total14 <- cbind(Points14, Max14)
Shots.Total14 <- Shots.Total14[,c(1,2,3,6)]

Shots.Total14$SV_PLAYER_ID <- as.factor(Shots.Total14$SV_PLAYER_ID)

Shots.Total14 <- inner_join(Shots.Total14, Player_Map, by = c("SV_PLAYER_ID"="SV_Player_id"))

Shots.Total14$PTS <- as.numeric(Shots.Total14$PTS)
Shots.Total14$Player_shots <- as.numeric(Shots.Total14$Player_shots)

Shots.Total14$Shot.Average <- round(Shots.Total14$PTS/Shots.Total14$Player_shots, digits =2)

# Points Total

Shots2014$Player_shots.total <- with(Shots2014, ave(as.character(SV_PLAYER_ID), SV_PLAYER_ID , FUN= seq_along))
Points.total14 <- aggregate(PTS ~ SV_PLAYER_ID, Shots2014, sum)
Max.total14 <- aggregate(Player_shots.total ~ SV_PLAYER_ID, Shots2014, max)
Player.Shots14 <- cbind(Points.total14, Max.total14)
Player.Shots14 <- Player.Shots14[,c(1,2,4)]
Player.Shots14$PTS <- as.numeric(Player.Shots14$PTS)
Player.Shots14$Player_shots.total <- as.numeric(Player.Shots14$Player_shots.total)
Player.Shots14$AVG.total <- round(Player.Shots14$PTS/ Player.Shots14$Player_shots.total, digits=2)
Player.Shots14 <- Player.Shots14[,c(1,4)]



# 2015 -----------

Shots2015<- inner_join(shot2015, Player_Map, by = c("SV_PLAYER_ID" = "SV_Player_id"))

Shots2015$Player_shots <- with(Shots2015, ave(as.character(GAME_ID), SV_PLAYER_ID , FUN= seq_along))

Points15 <- aggregate(PTS ~ GAME_ID + SV_PLAYER_ID, Shots2015, sum)

Max15 <- aggregate(Player_shots ~ SV_PLAYER_ID + GAME_ID, Shots2015, max)

Points15 <- Points15[order(Points15$GAME_ID, Points15$SV_PLAYER_ID),]
Max15 <- Max15[order(Max15$GAME_ID, Max15$SV_PLAYER_ID),]

Shots.Total15 <- cbind(Points15, Max15)
Shots.Total15 <- Shots.Total15[,c(1,2,3,6)]

Shots.Total15$SV_PLAYER_ID <- as.factor(Shots.Total15$SV_PLAYER_ID)

Shots.Total15 <- inner_join(Shots.Total15, Player_Map, by = c("SV_PLAYER_ID"="SV_Player_id"))

Shots.Total15$PTS <- as.numeric(Shots.Total15$PTS)
Shots.Total15$Player_shots <- as.numeric(Shots.Total15$Player_shots)

Shots.Total15$Shot.Average <- round(Shots.Total15$PTS/Shots.Total15$Player_shots, digits =2)

Shots.Total15 <- inner_join(Shots.Total15, Player.Shots14, by = c("SV_PLAYER_ID" = "SV_PLAYER_ID"))
Shots.Total15 <- inner_join(Shots.Total15, SD14, by = c("SV_PLAYER_ID" = "SV_PLAYER_ID"))

Shots.Total15$Plus.avg <- ifelse(Shots.Total15$Shot.Average < Shots.Total15$AVG.total + Shots.Total15$SD14 & Shots.Total15$Shot.Average > Shots.Total15$AVG.total -Shots.Total15$SD14, 0, 
                                 ifelse(Shots.Total15$Shot.Average > Shots.Total15$AVG.total, 1, -1))

Shots.Total15 <- inner_join(Shots.Total15, playbyplay15, by = c("GAME_ID" ="Game_id"))
Shots.Total15.Paul <- Shots.Total15[Shots.Total15$Name == "Paul Millsap",]
Shots.Total15.Lebron$GAME_ID <- as.factor(Shots.Total15.Lebron$GAME_ID)
ggplot(Shots.Total15.Paul, aes( x = Date, y = Plus.avg)) +geom_point()

# Points Total
Shots2015$Player_shots.total <- with(Shots2015, ave(as.character(SV_PLAYER_ID), SV_PLAYER_ID , FUN= seq_along))
Points.total15 <- aggregate(PTS ~ SV_PLAYER_ID, Shots2015, sum)
Max.total15 <- aggregate(Player_shots.total ~ SV_PLAYER_ID, Shots2015, max)
Player.Shots15 <- cbind(Points.total15, Max.total15)
Player.Shots15 <- Player.Shots15[c(1,2,4),]
Player.Shots15$PTS <- as.numeric(Player.Shots15$PTS)
Player.Shots15$Player_shots.total <- as.numeric(Player.Shots15$Player_shots.total)
Player.Shots15$AVG.total <- round(Player.Shots15$PTS/ Player.Shots15$Player_shots.total, digits=2)
Player.Shots15 <- Player.Shots15[,c(1,5)]
SD15 <- aggregate(PTS ~ SV_PLAYER_ID, Shots.Total15, sd, na.rm=T)


# 2016 -----------
Shots2016<- inner_join(shot2016, Player_Map, by = c("SV_PLAYER_ID" = "SV_Player_id"))

Shots2016$Player_shots <- with(Shots2016, ave(as.character(GAME_ID), SV_PLAYER_ID , FUN= seq_along))

Points16 <- aggregate(PTS ~ GAME_ID + SV_PLAYER_ID, Shots2016, sum)

Max16 <- aggregate(Player_shots ~ SV_PLAYER_ID + GAME_ID, Shots2016, max)

Points16 <- Points16[order(Points16$GAME_ID, Points16$SV_PLAYER_ID),]
Max16 <- Max16[order(Max16$GAME_ID, Max16$SV_PLAYER_ID),]

Shots.Total16 <- cbind(Points16, Max16)
Shots.Total16 <- Shots.Total16[,c(1,2,3,6)]

Shots.Total16$SV_PLAYER_ID <- as.factor(Shots.Total16$SV_PLAYER_ID)

Shots.Total16 <- inner_join(Shots.Total16, Player_Map, by = c("SV_PLAYER_ID"="SV_Player_id"))

Shots.Total16$PTS <- as.numeric(Shots.Total16$PTS)
Shots.Total16$Player_shots <- as.numeric(Shots.Total16$Player_shots)

Shots.Total16$Shot.Average <- round(Shots.Total16$PTS/Shots.Total16$Player_shots, digits =2)

Shots.Total16 <- inner_join(Shots.Total16, Player.Shots15, by = c("SV_PLAYER_ID" = "SV_PLAYER_ID"))
