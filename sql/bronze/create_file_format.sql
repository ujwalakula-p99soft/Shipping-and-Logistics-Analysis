CREATE FILE FORMAT IF NOT EXISTS SHIPPING_DB.BRONZE.CSV_FILE_FORMAT
    TYPE                        = CSV
    FIELD_DELIMITER             = ','
    SKIP_HEADER                 = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF                     = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL         = TRUE
    TRIM_SPACE                  = TRUE;
