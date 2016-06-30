-- Create syntax for TABLE 'player'
CREATE TABLE `player` (
  `cfn_id` bigint unsigned NOT NULL COMMENT 'player cfn id',
  `name` varchar(64) COLLATE utf8mb4_bin NOT NULL COMMENT 'The UID of the target object',
  `subscribed` tinyint(1) unsigned NOT NULL COMMENT 'whether this player is subscribed',
  `updated_at` timestamp NULL DEFAULT NULL COMMENT 'last time that match data was updated',
  `region` varchar(3) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'three characters region code',
  `platform` varchar(5) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'platform used to play game',
  `match_updated_at` timestamp NULL DEFAULT NULL COMMENT 'last time that match data was updated',
  `match_latest_ticks` bigint unsigned NULL DEFAULT NULL COMMENT 'latest match ticks from cfn',
  `match_data` text NULL DEFAULT NULL COMMENT 'aggregated data',
  `match_character` tinyint(6) DEFAULT NULL COMMENT 'most used character according to match data',
  PRIMARY KEY (`cfn_id`),
  KEY `IDX_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=COMPRESSED COMMENT='player data';

-- Create syntax for TABLE 'match'
CREATE TABLE `match` (
  `cfn_id` bigint unsigned NOT NULL COMMENT 'cfn match id',
  `left_player_cfn_id` bigint unsigned NOT NULL COMMENT 'left player cfn id',
  `right_player_cfn_id` bigint unsigned NOT NULL COMMENT 'right player cfn id',
  `data` text NOT NULL COMMENT 'full response json',
  PRIMARY KEY (`cfn_id`),
  KEY `IDX_left_player_cfn_id` (`left_player_cfn_id`),
  KEY `IDX_right_player_cfn_id` (`right_player_cfn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=COMPRESSED COMMENT='match data';

-- Create syntax for TABLE 'rank'
CREATE TABLE `rank` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `player_cfn_id` bigint unsigned NOT NULL COMMENT 'player cfn id',
  `placement` int unsigned NOT NULL COMMENT 'placement in ranking',
  `league_points` integer NOT NULL COMMENT 'league points',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'timestamp',
  `favorite_character` tinyint(6) DEFAULT NULL COMMENT 'favorite character',
  PRIMARY KEY (`id`),
  KEY `IDX_player_cfn_id` (`player_cfn_id`),
  CONSTRAINT `FK_player_cfn_id` FOREIGN KEY (`player_cfn_id`) REFERENCES `player` (`cfn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=COMPRESSED COMMENT='ranking data';
