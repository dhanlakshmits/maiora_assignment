-- Table: masterdata.tasks

-- DROP TABLE IF EXISTS masterdata.tasks;

CREATE TABLE IF NOT EXISTS masterdata.tasks
(
    task_id uuid NOT NULL DEFAULT masterdata.uuid_generate_v1mc(),
    task_name character varying COLLATE pg_catalog."default",
    task_duration character varying COLLATE pg_catalog."default",
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    task_start_date character varying COLLATE pg_catalog."default",
    task_end_date character varying COLLATE pg_catalog."default",
    user_id character varying COLLATE pg_catalog."default",
    CONSTRAINT task_pkey PRIMARY KEY (task_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS masterdata.tasks
    OWNER to postgres;


-- Table: masterdata.users

-- DROP TABLE IF EXISTS masterdata.users;

CREATE TABLE IF NOT EXISTS masterdata.users
(
    id uuid NOT NULL DEFAULT masterdata.uuid_generate_v1mc(),
    user_name character varying COLLATE pg_catalog."default" NOT NULL,
    user_email character varying COLLATE pg_catalog."default" NOT NULL,
    user_id character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS masterdata.users
    OWNER to postgres;

-- FUNCTION: masterdata.uuid_generate_v1mc()

-- DROP FUNCTION IF EXISTS masterdata.uuid_generate_v1mc();

CREATE OR REPLACE FUNCTION masterdata.uuid_generate_v1mc(
	)
    RETURNS uuid
    LANGUAGE 'c'
    COST 1
    VOLATILE STRICT PARALLEL SAFE 
AS '$libdir/uuid-ossp', 'uuid_generate_v1mc'
;

ALTER FUNCTION masterdata.uuid_generate_v1mc()
    OWNER TO postgres;


-- FUNCTION: masterdata.create_task(character varying, character varying, character varying, character varying, character varying)

-- DROP FUNCTION IF EXISTS masterdata.create_task(character varying, character varying, character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION masterdata.create_task(
	_user_id character varying,
	_task_name character varying,
	_task_duration character varying,
	_task_start_date character varying,
	_task_end_date character varying)
    RETURNS character varying
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
                                                
    Declare
		__user_id character varying;
    
	BEGIN

       select _user_id into  __user_id 
	   from masterdata.users where user_id=_user_id;
	   
	   if __user_id is not null then
		  
		  INSERT INTO masterdata.tasks(
			task_name, task_duration, user_id, task_start_date, task_end_date)
			VALUES (_task_name,_task_duration,_user_id,_task_start_date,_task_end_date);
			RETURN 'successfully inserted';
  		
		else
		
		  RETURN 'failed';
		 
		end if;
	 END;
$BODY$;

ALTER FUNCTION masterdata.create_task(character varying, character varying, character varying, character varying, character varying)
    OWNER TO postgres;


-- FUNCTION: masterdata.delete_task(character varying, character varying)

-- DROP FUNCTION IF EXISTS masterdata.delete_task(character varying, character varying);

CREATE OR REPLACE FUNCTION masterdata.delete_task(
	_user_id character varying,
	_task_name character varying)
    RETURNS character varying
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
                                                
    Declare
		__user_id character varying;
    
	BEGIN

       select _user_id into  __user_id 
	   from masterdata.users where user_id=_user_id;
	   
	   if __user_id is not null then
	   	
			if _task_name is not null then 
	   		  --delete based on task name
			  delete from masterdata.tasks
			  where user_id=_user_id and task_name=_task_name;

			  RETURN 'successfully deleted';
			  
			else
				--bulk delete
				delete from masterdata.tasks
				where user_id=_user_id;
				
				RETURN 'successfully deleted';
				
			end if;
  		
		else
		
		  RETURN 'failed';
		 
		end if;
	 END;
$BODY$;

ALTER FUNCTION masterdata.delete_task(character varying, character varying)
    OWNER TO postgres;


-- FUNCTION: masterdata.get_task(character varying, character varying)

-- DROP FUNCTION IF EXISTS masterdata.get_task(character varying, character varying);

CREATE OR REPLACE FUNCTION masterdata.get_task(
	_user_id character varying,
	_task_name character varying)
    RETURNS refcursor
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
                                                
    Declare
		ref refcursor default 'taskrefcursor';
		__user_id character varying;
    
	BEGIN

       select _user_id into  __user_id 
	   from masterdata.users where user_id=_user_id;
	   
	   if __user_id is not null then
	   
	   		if _task_name is not null then 
				OPEN ref FOR 
				  select task_name,task_duration,user_id,task_start_date,task_end_date from masterdata.tasks
				  where user_id=_user_id and task_name=_task_name;

				  RETURN ref;
			 
			 else
				 OPEN ref FOR 
			 	 select task_name,task_duration,user_id,task_start_date,task_end_date from masterdata.tasks
				 where user_id=_user_id;
		  
		  		RETURN ref;
				
			end if;
  		
		else
		
		  OPEN ref FOR 
		  SELECT null AS task_name, null AS task_duration, null AS user_id, null AS task_start_date, null AS task_end_date WHERE false;
			RETURN ref;
		 
		end if;
	 END;
$BODY$;

ALTER FUNCTION masterdata.get_task(character varying, character varying)
    OWNER TO postgres;


-- FUNCTION: masterdata.update_task(character varying, character varying, character varying, character varying, character varying)

-- DROP FUNCTION IF EXISTS masterdata.update_task(character varying, character varying, character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION masterdata.update_task(
	_user_id character varying,
	_task_name character varying,
	_task_duration character varying,
	_task_start_date character varying,
	_task_end_date character varying)
    RETURNS character varying
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    -- Check if the user exists
    IF EXISTS (SELECT 1 FROM masterdata.users WHERE user_id = _user_id) THEN
        -- Update the task
        UPDATE masterdata.tasks
        SET
            task_name = COALESCE(NULLIF(_task_name, ''), task_name),
            task_duration = COALESCE(NULLIF(_task_duration, ''), task_duration),
            task_start_date = COALESCE(NULLIF(_task_start_date, ''), task_start_date),
            task_end_date = COALESCE(NULLIF(_task_end_date, ''), task_end_date)
        WHERE
            user_id = _user_id;

        RETURN 'successfully updated';
    ELSE
        RETURN 'failed: user not found';
    END IF;
END;
$BODY$;

ALTER FUNCTION masterdata.update_task(character varying, character varying, character varying, character varying, character varying)
    OWNER TO postgres;
