create table PMU_AVAILABILITY
(
    ID NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY,
    DATA_DATE DATE NOT NULL,
    PMU_LOCATION VARCHAR2(250 BYTE) NOT NULL,
    AVAILABILITY_PERC NUMBER,
    DATA_VALID_PERC NUMBER,
    DATA_ERROR_PERC NUMBER,
    GPS_LOCKED_PERC NUMBER,
    UNIQUE(DATA_DATE, PMU_LOCATION)
);