CREATE TABLE Country (
  CountryID INT PRIMARY KEY,
  CountryName VARCHAR(255)
);

CREATE TABLE Teams (
  TeamID INT PRIMARY KEY,
  TeamName VARCHAR(255),
  TeamGender VARCHAR(255),
  TeamGroup VARCHAR(255),
  CountryID INT,

  FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);

CREATE TABLE Managers (
  ManagerID INT PRIMARY KEY,
  ManagerName VARCHAR(255),
  Nickname VARCHAR(255),
  DateOfBirth DATE,
  CountryID INT,
  FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);

CREATE TABLE TeamManagers (
  TeamID INT,
  ManagerID INT,
  FOREIGN KEY (TeamID) REFERENCES Teams(TeamID),
  FOREIGN KEY (ManagerID) REFERENCES Managers(ManagerID)
);

CREATE TABLE Stadiums (
  StadiumID INT PRIMARY KEY,
  StadiumName VARCHAR(255),
  CountryID INT,
  FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);

CREATE TABLE Referees (
  RefereeID INT PRIMARY KEY,
  RefereeName VARCHAR(255),
  CountryID INT,
  FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);

CREATE TABLE Competitions (
  CompetitionID INT,
  SeasonID INT,
  CountryName VARCHAR(255),
  CompetitionName VARCHAR(255),
  CompetitionGender VARCHAR(255),
  CompetitionYouth BOOLEAN,
  CompetitionInternational BOOLEAN,
  SeasonName VARCHAR(255),
  MatchUpdated TIMESTAMP WITH TIME ZONE,
  MatchUpdated360 TIMESTAMP WITH TIME ZONE,
  MatchAvailable TIMESTAMP WITH TIME ZONE,
  MatchAvailable360 TIMESTAMP WITH TIME ZONE,
  PRIMARY KEY (CompetitionID, SeasonID)
);

CREATE TABLE Matches (
  MatchID INT PRIMARY KEY,
  MatchDate DATE,
  KickOff TIME(3),
  CompetitionID INT, 
  SeasonID INT,
  HomeTeam INT,
  AwayTeam INT,
  HomeScore INT,
  AwayScore INT,
  MatchStatus VARCHAR(255),
  MatchStatus360 VARCHAR(255),
  LastUpdated TIMESTAMP,
  LastUpdated360 TIMESTAMP,
  MatchWeek INT,
  CompetitionStage INT,  
  Stadium INT,
  Referee INT,

  FOREIGN KEY (CompetitionID, SeasonID) REFERENCES Competitions(CompetitionID, SeasonID),
  FOREIGN KEY (HomeTeam) REFERENCES Teams(TeamID),
  FOREIGN KEY (AwayTeam) REFERENCES Teams(TeamID),
  FOREIGN KEY (Stadium) REFERENCES Stadiums(StadiumID),
  FOREIGN KEY (Referee) REFERENCES Referees(RefereeID)
);

CREATE TABLE Metadata (
  MatchID INT PRIMARY KEY,
  DataVersion VARCHAR(255),
  ShotFidelityVersion VARCHAR(255),
  XYFidelityVersion VARCHAR(255),

  FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
);

CREATE TABLE Lineups (
  MatchID INT,
  TeamID INT,
  PRIMARY KEY (MatchID, TeamID),
  FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
  FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);

CREATE TABLE Players (
  PlayerID INT PRIMARY KEY,
  MatchID INT,
  TeamID INT,
  JerseyNumber INT,
  CountryID INT,
  PlayerName VARCHAR(255),
  Nickname VARCHAR(255),

  FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
  FOREIGN KEY (MatchID, TeamID) REFERENCES Lineups(MatchID, TeamID),
  FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);

CREATE TABLE PlayerPositions (
  PlayerPositionID SERIAL,
  MatchID INT,
  PlayerID INT,
  PositionID INT,
  SwitchedFrom VARCHAR(255),
  SwitchedTo VARCHAR(255),
  FromPeriod INT,
  ToPeriod INT,
  StartReason VARCHAR(255),
  EndReason VARCHAR(255),

  PRIMARY KEY (PlayerPositionID, MatchID, PlayerID)

);

CREATE TABLE LineupPlayerCard (
  MatchID INT,
  PlayerID INT,
  CardTime VARCHAR(255),
  CardType VARCHAR(255),
  Reason VARCHAR(255),
  Period INT,

  PRIMARY KEY (MatchID, PlayerID, CardTime)
);

CREATE TABLE Events (
  EventID UUID PRIMARY KEY,
  MatchID INT,
  Index INT,
  Period INT,
  Timestamp TIME,
  Minute INT,
  Second INT,
  EventType INT,
  EventTypeName VARCHAR(255),
  Possession INT,
  PossessionTeamID INT,
  PossessionTeamName VARCHAR(255),
  PlayPatternID INT,
  PlayPatternName VARCHAR(255),
  TeamID INT,
  TeamName VARCHAR(255),
  PlayerID INT,
  PlayerName VARCHAR(255),
  PositionID INT,
  PositionName VARCHAR(255),
  LocationX DOUBLE PRECISION,
  LocationY DOUBLE PRECISION,
  Duration DECIMAL,
  UnderPressure BOOLEAN,
  OffCamera BOOLEAN,
  Out BOOLEAN,
  RelatedEvents UUID[],

  FOREIGN KEY (PossessionTeamID) REFERENCES Teams(TeamID),
  FOREIGN KEY (TeamID) REFERENCES Teams(TeamID),
  FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
  FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
);

CREATE TABLE Tactics (
  EventID UUID PRIMARY KEY,
  Formation INT,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE TacticLineupPlayer (
  TacticID UUID PRIMARY KEY,
  PlayerID INT,
  PositionID INT,

  FOREIGN KEY (TacticID) REFERENCES Tactics(EventID),
  FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
  
);

CREATE TABLE ThreeSixty (
  ThreeSixtyID UUID PRIMARY KEY,
  VisibleArea DOUBLE PRECISION[],

  FOREIGN KEY (ThreeSixtyID) REFERENCES Events(EventID)
);

CREATE TABLE FreezeFrames (
  ThreeSixtyID UUID,
  Teammate BOOLEAN,
  Actor BOOLEAN,
  Keeper BOOLEAN,
  LocationX DOUBLE PRECISION,
  LocationY DOUBLE PRECISION,
  LocationZ DOUBLE PRECISION,

  FOREIGN KEY (ThreeSixtyID) REFERENCES Events(EventID)
);

-- Event Tables --
CREATE TABLE FiftyFifty (
  EventID UUID,
  OutcomeID INT,
  OutcomeName VARCHAR(255),
  Counterpress BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE BadBehaviour (
  EventID UUID,
  CardID INT,
  CardName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE BallReceipt (
  EventID UUID,
  OutcomeID INT,
  OutcomeName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE BallRecovery (
  EventID UUID,
  Offensive BOOLEAN,
  RecoveryFailure BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Block (
  EventID UUID,
  Deflection BOOLEAN,
  Offensive BOOLEAN,
  SaveBlock BOOLEAN,
  Counterpress BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Carry (
  EventID UUID,
  EndLocationX DOUBLE PRECISION,
  EndLocationY DOUBLE PRECISION,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Clearance (
  EventID UUID,
  AerialWon BOOLEAN,
  BodyPartID INT,
  BodyPartName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Dribble (
  EventID UUID,
  Overrun BOOLEAN,
  Nutmeg BOOLEAN,
  OutcomeID INT,
  OutcomeName VARCHAR(255),
  NoTouch BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE DribbledPast (
  EventID UUID,
  Counterpress BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Duel (
  EventID UUID,
  Counterpress BOOLEAN,
  TypeID INT,
  TypeName VARCHAR(255),
  OutcomeID INT,
  OutcomeName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE FoulCommitted (
  EventID UUID,
  Counterpress BOOLEAN,
  Offensive BOOLEAN,
  TypeID INT,
  TypeName VARCHAR(255),
  Advantage BOOLEAN,
  Penalty BOOLEAN,
  CardID INT,
  CardName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE FoulWon (
  EventID UUID,
  Defensive BOOLEAN,
  Advantage BOOLEAN,
  Penalty BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Goalkeeper (
  EventID UUID,
  PositionID INT,
  PositionName VARCHAR(255),
  TechniqueID INT,
  TechniqueName VARCHAR(255),
  BodyPartID INT,
  TypeID INT,
  TypeName VARCHAR(255),
  OutcomeID INT,
  OutcomeName VARCHAR(255),
  BodyPartName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE HalfEnd (
  EventID UUID,
  EarlyVideoEnd BOOLEAN,
  MatchSuspended BOOLEAN,
  
  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE HalfStart (
  EventID UUID,
  LateVideoStart BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE InjuryStoppage (
  EventID UUID,
  InChain BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Interception (
  EventID UUID,
  OutcomeID INT,
  OutcomeName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Miscontrol (
  EventID UUID,
  AerialWon BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Pass (
  EventID UUID,
  Recipient INT,
  Length DECIMAL,
  Angle DECIMAL,
  HeightID INT,
  HeightName VARCHAR(255),
  EndLocationX DOUBLE PRECISION,
  EndLocationY DOUBLE PRECISION,
  AssisstedShot UUID,
  Backheel BOOLEAN,
  Deflected BOOLEAN,
  Miscommunication BOOLEAN,
  IsCross BOOLEAN,
  CutBack BOOLEAN,
  Switch BOOLEAN,
  ShotAssist BOOLEAN,
  GoalAssist BOOLEAN,
  BodyPartID INT,
  BodyPartName VARCHAR(255),
  TypeID INT,
  TypeName VARCHAR(255),
  OutcomeID INT,
  OutcomeName VARCHAR(255),
  TechniqueID INT,
  TechniqueName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID),
  FOREIGN KEY (Recipient) REFERENCES Players(PlayerID)
);

CREATE TABLE PlayerOff (
  EventID UUID,
  Permanent BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Pressure (
  EventID UUID,
  Counterpress BOOLEAN,

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Shot (
  EventID UUID,
  KeyPassID UUID UNIQUE,
  EndLocationX DOUBLE PRECISION,
  EndLocationY DOUBLE PRECISION, 
  EndLocationZ DOUBLE PRECISION,
  AerialWon BOOLEAN,
  FollowsDribble BOOLEAN,
  FirstTime BOOLEAN,
  OpenGoal BOOLEAN,
  StatsbombXG DECIMAL,
  Deflected BOOLEAN,
  TechniqueID INT,
  TechniqueName VARCHAR(255),
  BodyPartID INT,
  BodyPartName VARCHAR(255),
  TypeID INT,
  TypeName VARCHAR(255),
  OutcomeID INT,
  OutcomeName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE FreezeFrame (
  EventID UUID,
  LocationX DOUBLE PRECISION,
  LocationY DOUBLE PRECISION,
  LocationZ DOUBLE PRECISION,
  Player INT,
  PositionID INT,
  Teammate BOOLEAN,
  OutcomeID INT,
  OutcomeName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID),
  FOREIGN KEY (Player) REFERENCES Players(PlayerID)
);

CREATE TABLE Substitution (
  EventID UUID,
  Replacement INT,
  OutcomeID INT,
  OutcomeName VARCHAR(255),

  FOREIGN KEY (EventID) REFERENCES Events(EventID),
  FOREIGN KEY (Replacement) REFERENCES Players(PlayerID)
);

ALTER TABLE Managers ADD CONSTRAINT unique_manager_id_name UNIQUE (ManagerID, ManagerName);
ALTER TABLE Country ADD CONSTRAINT unique_country_id_name UNIQUE (CountryID, CountryName);
ALTER TABLE Referees ADD CONSTRAINT unique_referee_id_name UNIQUE (RefereeID, RefereeName);
ALTER TABLE Stadiums ADD CONSTRAINT unique_stadium_id_name UNIQUE (StadiumID, StadiumName);
ALTER TABLE Teams ADD CONSTRAINT unique_team_id_name UNIQUE (TeamID, TeamName);
ALTER TABLE Metadata ADD CONSTRAINT unique_metadata_id UNIQUE (MatchID, DataVersion, ShotFidelityVersion, XYFidelityVersion);
ALTER TABLE Events ADD CONSTRAINT unique_EventID UNIQUE (EventID);
ALTER TABLE Players ADD CONSTRAINT unique_player_id UNIQUE (PlayerID);
ALTER TABLE Lineups ADD CONSTRAINT unique_lineup_id UNIQUE (MatchID, TeamID);
ALTER TABLE PlayerPositions ADD CONSTRAINT unique_player_position_id UNIQUE (PlayerPositionID, MatchID, PlayerID);