--drop views
DROP VIEW IF EXISTS doe_scores;
DROP VIEW IF EXISTS alive_sessions;
DROP VIEW IF EXISTS alive_does;

-- View for all alive does
CREATE VIEW alive_does AS
	SELECT * FROM animal
	WHERE status='Current'
	AND sex='Female';

-- View for joined session and does
CREATE VIEW alive_sessions AS
	SELECT * FROM alive_does
	NATURAL JOIN session_animal;

-- Example, get average birth weight per alive doe
SELECT animal_id,tag,AVG(birth_weight) FROM alive_sessions
	GROUP BY animal_id,tag;

-- Example, view for the doe scores
CREATE VIEW doe_scores AS
	SELECT animal_id,tag,session_id,
		CASE WHEN birth_weight > 6 THEN 5 ELSE 3 END +
		CASE WHEN mothering = 'Good Mom' THEN 5 ELSE 1 END +
		CASE WHEN milk_rating = '1 Good Milk' THEN 5 ELSE 1 END +
		CASE WHEN num_of_kids = '2 Twins' THEN 4
			WHEN num_of_kids = '3 Triplets' THEN 3
			ELSE 2
		END AS score
	FROM alive_sessions;

-- Example, rank does by score
SELECT animal_id,tag,SUM(score),AVG(score) FROM doe_scores
	GROUP BY animal_id,tag
	ORDER BY AVG(score) DESC;
