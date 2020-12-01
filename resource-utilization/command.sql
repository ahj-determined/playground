Copy (SELECT experiment_id, username, slots, start_time, training_time_sec
FROM
(SELECT id as experiment_id, 
        owner_id,
        (e.config->'description') as description, 
        (e.config->'resources'->>'slots_per_trial')::int as slots,
        (select coalesce(extract(epoch from sum(steps.end_time - steps.start_time)), 0) 
          FROM steps, trials
          WHERE trials.experiment_id = e.id AND steps.trial_id = trials.id) as training_time_sec,
        (select coalesce(extract(epoch from sum(v.end_time - v.start_time)), 0)
          FROM validations v, trials t
          WHERE t.experiment_id = e.id AND v.trial_id = t.id) AS validation_time_sec,
        (select coalesce(extract(epoch from sum(c.end_time - c.start_time)), 0)
          FROM checkpoints c, trials t
          WHERE t.experiment_id = e.id AND c.trial_id = t.id) AS checkpoint_time_sec,
        start_time,
        end_time,
        (end_time - start_time) as wall_time,
        state
FROM experiments e) exp
JOIN
(SELECT id as user_id, username
FROM users) usr
ON exp.owner_id = usr.user_id
ORDER BY experiment_id ASC) To '/tmp/test.csv' With CSV DELIMITER ',' HEADER;

