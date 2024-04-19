-- View for all alive does
DROP VIEW alive_does;
CREATE VIEW alive_does AS
	SELECT * FROM animal
	WHERE status='Current'
	AND sex='Female';

-- View for joined session and does
DROP VIEW alive_sessions;
CREATE VIEW alive_sessions AS
	SELECT * FROM alive_does
	NATURAL JOIN session_animal;
