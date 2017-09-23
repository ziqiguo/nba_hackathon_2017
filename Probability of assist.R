# Load Packages
install.packages("pacman")
library(pacman)
pacman::p_load(dplyr, readr, data.table, car, glmnet, ROCR)

# Read in Data and clean ---------

# 2014 ---------
shot2014 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2014-15_nba_shot_log.txt", 
                                      "\t", escape_double = FALSE, trim_ws = TRUE)

shot2014 <- as.data.frame(shot2014)

shot2014$GAME_ID <- as.integer(shot2014$GAME_ID)

# Order in increasing order by game id, period, and decreasing by game clock

shot2014 <- shot2014[
  order( shot2014$GAME_ID, shot2014$PERIOD, -shot2014$GAME_CLOCK ),
  ]

# Create counter for shots taken
shot2014$shot_count <- with(shot2014, ave(as.character(GAME_ID), GAME_ID, FUN= seq_along))

# Repeat for 2015 ----------

shot2015 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2015-16_nba_shot_log.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)

shot2015 <- as.data.frame(shot2015)

shot2015$GAME_ID <- as.integer(shot2015$GAME_ID)

shot2015 <- shot2015[
  order( shot2015$GAME_ID, shot2015$PERIOD, -shot2015$GAME_CLOCK ),
  ]

shot2015$shot_count <- with(shot2015, ave(as.character(GAME_ID), GAME_ID, FUN= seq_along))


# Repeat for 2016 ---------

shot2016 <- read_delim("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/Player Tracking Data/2016-17_nba_shot_log.txt", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)

shot2016 <- as.data.frame(shot2016)

shot2016$GAME_ID <- as.integer(shot2016$GAME_ID)

shot2016 <- shot2016[
  order( shot2016$GAME_ID, shot2016$PERIOD, -shot2016$GAME_CLOCK ),
  ]

shot2016$shot_count <- with(shot2016, ave(as.character(GAME_ID), GAME_ID, FUN= seq_along))

# Read in play by play data ----------

playbyplay <- fread("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/data/Play_by_Play_New.csv") 

# Filter by year ----------

#2014
playbyplay14 <- playbyplay[playbyplay$Season==2014,]
playbyplay14 <- playbyplay14[playbyplay14$Season_Type=="Regular",]

# Only Consider Shots

playbyplay14 <- playbyplay14[playbyplay14$Shot_Outcome == 1 | playbyplay14$Shot_Outcome == 0, ]

# Create shot counter
playbyplay14$shot_count <- with(playbyplay14, ave(as.character(Game_id), Game_id, FUN= seq_along))

# Repeat for 2015 ----------
playbyplay15 <- playbyplay[playbyplay$Season==2015,]
playbyplay15 <- playbyplay15[playbyplay15$Season_Type=="Regular",]

playbyplay15 <- playbyplay15[playbyplay15$Shot_Outcome == 1 | playbyplay15$Shot_Outcome == 0, ]

playbyplay15$shot_count <- with(playbyplay15, ave(as.character(Game_id), Game_id, FUN= seq_along))

# Repeat for 2016 ----------

playbyplay16 <- playbyplay[playbyplay$Season==2016,]
playbyplay16 <- playbyplay16[playbyplay16$Season_Type=="Regular",]

playbyplay16 <- playbyplay16[playbyplay16$Shot_Outcome == 1 | playbyplay16$Shot_Outcome == 0, ]

playbyplay16$shot_count <- with(playbyplay16, ave(as.character(Game_id), Game_id, FUN= seq_along))

# Merge Files

# Merge by game id and shot count

Assist14 <- playbyplay14 %>%
  inner_join(shot2014, by= c("Game_id"="GAME_ID", "shot_count"= "shot_count"))

Assist15 <- playbyplay15 %>%
  inner_join(shot2015, by= c("Game_id"="GAME_ID", "shot_count"= "shot_count"))

Assist16 <- playbyplay16 %>%
  inner_join(shot2016, by= c("Game_id"="GAME_ID", "shot_count"= "shot_count"))

# Only Consider Shots Made 

Assist14 <- Assist14[Assist14$Shot_Outcome == 1,]
Assist15 <- Assist15[Assist15$Shot_Outcome == 1,]
Assist16 <- Assist16[Assist16$Shot_Outcome == 1,]

# Create Assist Column ----------

Assist14$Assist <- +(grepl("assist", Assist14$Description, ignore.case=T))
Assist15$Assist <- +(grepl("assist", Assist15$Description, ignore.case=T))
Assist16$Assist <- +(grepl("assist", Assist16$Description, ignore.case=T))

# Model

# Combine 2014 and 2015 data
Assist14b <- Assist14[, c("DRIBBLES", "TOUCH_TIME", "Assist")]
Assist14b$d.tt <- Assist14b$DRIBBLES*Assist14b$TOUCH_TIME
Assist15b <- Assist15[, c("DRIBBLES", "TOUCH_TIME", "Assist")]
Assist15b$d.tt <- Assist15b$DRIBBLES*Assist15b$TOUCH_TIME
Assist16b <- Assist16[, c("DRIBBLES", "TOUCH_TIME", "Assist")]
Assist16b$d.tt <- Assist16b$DRIBBLES*Assist16b$TOUCH_TIME

Assist1415 <- rbind(Assist14b, Assist15b)

# Create Training and Testing Matrices for LASSO

assist.train <- Assist1415$Assist
xvars.train <- as.matrix(Assist1415[,c("DRIBBLES","TOUCH_TIME",  "d.tt")])
assist.test <- Assist16b$Assist
xvars.test <- as.matrix(Assist16b[,c("DRIBBLES","TOUCH_TIME", "d.tt")])

# Start with Basic GLM, too much correlation in data, no good model selection

glm1 <- glm(Assist ~ DRIBBLES+TOUCH_TIME, family= binomial(logit), data= Assist1415, na.action=na.omit)

# Lasso 
glm.lasso <- glmnet(x= xvars.train, y=assist.train, family="binomial")

# Selecting lambda via cross validation

cv.lasso <- cv.glmnet(x= xvars.train, y=assist.train,  family= "binomial")
coef(cv.lasso, s=cv.lasso$lambda.min)
coef(cv.lasso, s=cv.lasso$lambda.1se)

# Find AUC for different lambdas

# 1se 
Assist16b$predict1 <- predict(cv.lasso, s= cv.lasso$lambda.1se, newx = xvars.test, type = "response")
predictions.lasso1 <- prediction(Assist16b$predict1, Assist16b$Assist)
AUC1 <- performance(predictions.lasso1, measure = "auc" )
AUC1@y.values

# lambda min
Assist16b$predict2 <- predict(cv.lasso, s= cv.lasso$lambda.min, newx = xvars.test, type = "response")
predictions.lasso2 <- prediction(Assist16b$predict2, Assist16b$Assist)
AUC2 <- performance(predictions.lasso2, measure = "auc" )
AUC2@y.values

# 1 se slightly better 

# Print Coefficients 
coef(cv.lasso, s=cv.lasso$lambda.1se)
