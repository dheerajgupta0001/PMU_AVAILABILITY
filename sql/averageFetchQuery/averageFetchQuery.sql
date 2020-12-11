select pmu_location, AVG(availability_perc), COUNT(availability_perc) from mis_warehouse.pmu_availability
where data_date between '01-10-2020' and '31-10-2020'
group by pmu_location