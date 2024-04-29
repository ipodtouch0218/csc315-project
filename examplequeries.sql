--drop views
DROP VIEW IF EXISTS doe_status_scores;
DROP VIEW IF EXISTS tag_dam_join;
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
			ELSE 2 END +
		CASE WHEN observations = '1 No Problems' THEN 5 ELSE 1 END +
		CASE WHEN kid_ease = '1 No Assist' THEN 5 ELSE 1 END +
		CASE WHEN mother_score = '1 Doe stays close' THEN 5 ELSE 1
		END AS score
	FROM alive_sessions;

-- Example, rank does by score
SELECT animal_id,tag,SUM(score),AVG(score) FROM doe_scores
	GROUP BY animal_id,tag
	ORDER BY AVG(score) DESC;

-- Tag to Dam self-join from animal
CREATE VIEW tag_dam_join AS
	SELECT a1.tag, a1.animal_id, a2.dam, a2.status 
	FROM animal a1, animal a2
	WHERE a1.tag = a2.dam ORDER BY a1.tag;

--Status score by Doe
CREATE VIEW doe_status_scores AS
    SELECT animal_id, tag, SUM(status_points) AS status_score
    FROM 
        (SELECT animal_id, tag,
            CASE WHEN status = 'Current' THEN 5
            WHEN status = 'Sold' THEN 1 
            WHEN status = 'Dead' THEN -3
            ELSE 0
            END AS status_points 
        FROM tag_dam_join)
    GROUP BY tag, animal_id
    ORDER BY status_score DESC;

--Example, scores and status_scores
SELECT animal_id,tag,SUM(score), AVG(score), status_score 
FROM doe_scores NATURAL JOIN doe_status_scores 
GROUP BY animal_id, tag, status_score 
ORDER BY AVG(score) DESC;
