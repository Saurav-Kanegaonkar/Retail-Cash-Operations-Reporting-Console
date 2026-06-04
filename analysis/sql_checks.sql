-- Illustrative checks for Retail Cash Operations Reporting Console
select signal, owner, risk
from source_events
where risk in ('High', 'Medium');
