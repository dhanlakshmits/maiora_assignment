-- Table: masterdata.innoventes_emp

-- DROP TABLE IF EXISTS masterdata.innoventes_emp;

CREATE TABLE IF NOT EXISTS masterdata.innoventes_emp
(
    "Id" uuid NOT NULL DEFAULT masterdata.uuid_generate_v1mc(),
    company_name character varying COLLATE pg_catalog."default" NOT NULL,
    email_id character varying COLLATE pg_catalog."default" NOT NULL,
    company_code character varying COLLATE pg_catalog."default",
    strength integer,
    website character varying COLLATE pg_catalog."default",
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    company_id character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT innoventes_emp_pkey PRIMARY KEY ("Id")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS masterdata.innoventes_emp
    OWNER to postgres;


-- FUNCTION: masterdata.create_company(character varying, character varying, character varying, integer, character varying, character varying)

-- DROP FUNCTION IF EXISTS masterdata.create_company(character varying, character varying, character varying, integer, character varying, character varying);

CREATE OR REPLACE FUNCTION masterdata.create_company(
	_company_name character varying,
	_email_id character varying,
	_company_code character varying,
	_strength integer,
	_website character varying,
	_company_id character varying)
    RETURNS character varying
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
                                                
    Declare
	__company_name character varying;
	__email_id character varying;
    
	BEGIN
	
	select company_name, email_id into __company_name, __email_id  from masterdata.innoventes_emp
	where company_name=_company_name and email_id=_email_id;
	
	if __company_name is null and __email_id is null then
	
		  	INSERT INTO masterdata.innoventes_emp(
			company_name, email_id, company_code, strength, website, company_id)
			VALUES (_company_name,_email_id,_company_code,_strength,_website,_company_id);
			RETURN 'successfully inserted';
	else
		return 'duplicate records found';
	end if;
  		
	 END;
$BODY$;

ALTER FUNCTION masterdata.create_company(character varying, character varying, character varying, integer, character varying, character varying)
    OWNER TO postgres;


-- FUNCTION: masterdata.update_company(character varying, character varying, character varying, character varying, character varying)

-- DROP FUNCTION IF EXISTS masterdata.update_company(character varying, character varying, character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION masterdata.update_company(
	_company_name character varying,
	_email_id character varying,
	_company_code character varying,
	_website character varying,
	_company_id character varying)
    RETURNS character varying
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    -- Check if the company_id exists
    IF EXISTS (SELECT 1 FROM masterdata.innoventes_emp WHERE company_id = _company_id) THEN
        -- Update the company details
        UPDATE masterdata.innoventes_emp
        SET
			company_name=COALESCE(NULLIF(_company_name, ''), company_name), 
			email_id=COALESCE(NULLIF(_email_id, ''), email_id), 
			company_code=COALESCE(NULLIF(_company_code, ''), company_code), 
-- 			strength=COALESCE(NULLIF(_strength, ''), strength), 
			website=COALESCE(NULLIF(_website, ''), website)
        WHERE
            company_id = _company_id;

        RETURN 'successfully updated';
    ELSE
        RETURN 'failed: company_id not found';
    END IF;
END;
$BODY$;

ALTER FUNCTION masterdata.update_company(character varying, character varying, character varying, character varying, character varying)
    OWNER TO postgres;


-- FUNCTION: masterdata.delete_company(character varying)

-- DROP FUNCTION IF EXISTS masterdata.delete_company(character varying);

CREATE OR REPLACE FUNCTION masterdata.delete_company(
	_company_id character varying)
    RETURNS character varying
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
                                                
    Declare
		__company_id character varying;
    
	BEGIN

       select company_id into  __company_id 
	   from masterdata.innoventes_emp where company_id=_company_id;
	   
	   if __company_id is not null then
	   	
			  delete from masterdata.innoventes_emp
			  where company_id=_company_id;

			  RETURN 'successfully deleted';
			  
		else
		
		  RETURN 'failed to delete: company_id not found';
		 
		end if;
	 END;
$BODY$;

ALTER FUNCTION masterdata.delete_company(character varying)
    OWNER TO postgres;


-- FUNCTION: masterdata.get_company(character varying, integer, integer)

-- DROP FUNCTION IF EXISTS masterdata.get_company(character varying, integer, integer);

CREATE OR REPLACE FUNCTION masterdata.get_company(
	_company_id character varying,
	_limit integer,
	_offset integer)
    RETURNS refcursor
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
                                                
    Declare
		ref refcursor default 'companyrefcursor';
		__company_id character varying;
    
	BEGIN

       select company_id into  __company_id 
	   from masterdata.innoventes_emp where company_id=_company_id;
	   
	   if __company_id is not null then
	   
				OPEN ref FOR 
				  select company_id, company_name, email_id, company_code, strength, website from masterdata.innoventes_emp
				  where company_id=_company_id limit _limit offset _offset; 

				  RETURN ref;
  		
		else
		
		  OPEN ref FOR 
		  SELECT null AS company_id, null AS company_name, null AS company_code, null AS strength, null AS website WHERE false;
			RETURN ref;
		 
		end if;
	 END;
$BODY$;

ALTER FUNCTION masterdata.get_company(character varying, integer, integer)
    OWNER TO postgres;


