
      
   
  USE [test_normalization];
  if object_id ('test_normalization."exchange_rate_temp_view"','V') is not null
      begin
      drop view test_normalization."exchange_rate_temp_view"
      end


   
   
  USE [test_normalization];
  if object_id ('test_normalization."exchange_rate"','U') is not null
      begin
      drop table test_normalization."exchange_rate"
      end


   USE [test_normalization];
   EXEC('create view test_normalization."exchange_rate_temp_view" as
    
-- Final base SQL model
select
    id,
    currency,
    "date",
    timestamp_col,
    "HKD@spéçiäl & characters",
    hkd_special___characters,
    nzd,
    usd,
    _airbyte_ab_id,
    _airbyte_emitted_at,
    SYSDATETIME() as _airbyte_normalized_at,
    _airbyte_exchange_rate_hashid
from "test_normalization"._airbyte_test_normalization."exchange_rate_ab3"
-- exchange_rate from "test_normalization".test_normalization._airbyte_raw_exchange_rate
where 1 = 1

    ');

   SELECT * INTO "test_normalization".test_normalization."exchange_rate" FROM
    "test_normalization".test_normalization."exchange_rate_temp_view"

   
   
  USE [test_normalization];
  if object_id ('test_normalization."exchange_rate_temp_view"','V') is not null
      begin
      drop view test_normalization."exchange_rate_temp_view"
      end

    
   use [test_normalization];
  if EXISTS (
        SELECT * FROM
        sys.indexes WHERE name = 'test_normalization_exchange_rate_cci'
        AND object_id=object_id('test_normalization_exchange_rate')
    )
  DROP index test_normalization.exchange_rate.test_normalization_exchange_rate_cci
  CREATE CLUSTERED COLUMNSTORE INDEX test_normalization_exchange_rate_cci
    ON test_normalization.exchange_rate

   


  