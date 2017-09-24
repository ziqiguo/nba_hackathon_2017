shot_and_assist_data <- read.csv("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/shot_and_assist_data.csv")
View(shot_and_assist_data)
shot_and_assist_data$GAME_ID <- as.factor(shot_and_assist_data$GAME_ID)
shot2016$GAME_ID <- as.factor(shot2016$GAME_ID)
Game.example.21600122<- shot_and_assist_data[shot_and_assist_data$GAME_ID ==21600122, ]
Game.example.21600122<-merge(x = Game.example.21600122, y = shot2016[ , c("PERSON_ID", "TEAM_ID")], by.x ="PLAYER_ID", by.y="PERSON_ID", all.x=TRUE)

Game.example.21600122 <- unique(Game.example.21600122)

# only because there was a row of NA for this example (look at data first)
Game.example.21600122 <- Game.example.21600122[-1,]

Team_Map <- read.csv("~/Desktop/Documents/Statistics/Hackathon/Competition/Hackathon/data/Team_Map.csv")
Game.example.21600122 <- inner_join(Game.example.21600122, Team_Map, by = c("TEAM_ID"="Team_ID"))
Game.example.21600122 <- inner_join(Game.example.21600122, Player_Map, by = c("PLAYER_ID"="Player_id"))

Game.example.21600122.Wizards <- Game.example.21600122[Game.example.21600122$Team =="Wizards",]
Game.example.21600122.Cavaliers <- Game.example.21600122[Game.example.21600122$Team =="Cavaliers",]

# Plotting
ggplot(Game.example.21600122.Wizards, aes(x=Name, y=Expected.Points.from.Assists)) + 
  geom_segment(aes(x=Name, 
                   xend=Name, 
                   y=Expected.Points.from.Assists, 
                   yend=Actual.Points.from.Assists), color= "darkgoldenrod") +
  geom_point(size=6, color="blue") + 
  labs(title="Predicted Vs. Actual Points from Assists") + geom_point(aes(x=Name, y=Actual.Points.from.Assists), size= 5, color = "red")+
  theme(axis.text.x = element_text(angle=65, vjust=0.6)) +ylab("")+ xlab("") +theme(axis.text.x=element_text(angle=45,hjust=1))+
  theme(panel.background=element_rect(fill='grey90'), panel.grid.minor = element_line(color= "grey"), panel.grid.major = element_line( size =0), plot.background = element_rect(fill="white"))

ggplot(Game.example.21600122.Cavaliers, aes(x=Name, y=Expected.Points.from.Assists)) + 
  geom_segment(aes(x=Name, 
                   xend=Name, 
                   y=Expected.Points.from.Assists, 
                   yend=Actual.Points.from.Assists), color= "darkgoldenrod") +
  geom_point(size=6, color="blue") + 
  labs(title="Predicted Vs. Actual Points from Assists") + geom_point(aes(x=Name, y=Actual.Points.from.Assists), size= 5, color = "red")+
  theme(axis.text.x = element_text(angle=65, vjust=0.6)) +ylab("")+ xlab("") +theme(axis.text.x=element_text(angle=45,hjust=1))+
  theme(panel.background=element_rect(fill='grey90'), panel.grid.minor = element_line(color= "grey"), panel.grid.major = element_line( size =0), plot.background = element_rect(fill="white"))

ggplot(Game.example.21600122.Wizards, aes(x=Name, y=Expected.Points)) + 
  geom_segment(aes(x=Name, 
                   xend=Name, 
                   y=Expected.Points, 
                   yend=Actual.Points), color= "darkgoldenrod") +
  geom_point(size=6, color="blue") + 
  labs(title="Predicted Vs. Actual Points") + geom_point(aes(x=Name, y=Actual.Points), size= 5, color = "red")+
  theme(axis.text.x = element_text(angle=65, vjust=0.6)) +ylab("")+ xlab("") +theme(axis.text.x=element_text(angle=45,hjust=1))+
  theme(panel.background=element_rect(fill='grey90'), panel.grid.minor = element_line(color= "grey"), panel.grid.major = element_line( size =0), plot.background = element_rect(fill="white"))

ggplot(Game.example.21600122.Cavaliers, aes(x=Name, y=Expected.Points)) + 
  geom_segment(aes(x=Name, 
                   xend=Name, 
                   y=Expected.Points, 
                   yend=Actual.Points), color= "darkgoldenrod") +
  geom_point(size=6, color="blue") + 
  labs(title="Predicted Vs. Actual Points") + geom_point(aes(x=Name, y=Actual.Points), size= 5, color = "red")+
  theme(axis.text.x = element_text(angle=65, vjust=0.6)) +ylab("")+ xlab("") +theme(axis.text.x=element_text(angle=45,hjust=1))+
  theme(panel.background=element_rect(fill='grey90'), panel.grid.minor = element_line(color= "grey"), panel.grid.major = element_line( size =0), plot.background = element_rect(fill="white"))

# Second Game Day

Game.example.21400651<- shot_and_assist_data[shot_and_assist_data$GAME_ID ==21400651, ]
Game.example.21400651<-merge(x = Game.example.21400651, y = shot2014[ , c("PERSON_ID", "TEAM_ID")], by.x ="PLAYER_ID", by.y="PERSON_ID", all.x=TRUE)

Game.example.21400651 <- unique(Game.example.21400651)
