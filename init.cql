CREATE KEYSPACE IF NOT EXISTS traffic_data WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE traffic_data;

CREATE TABLE IF NOT EXISTS alerts (
  id UUID PRIMARY KEY,
  country TEXT,
  city TEXT,
  reliability INT,
  type TEXT,
  uuid TEXT,
  speed INT,
  subtype TEXT,
  street TEXT,
  n_comments INT,
  inscale BOOLEAN,
  confidence INT,
  road_type INT,
  location_x DOUBLE,
  location_y DOUBLE,
  pub_millis BIGINT
);
