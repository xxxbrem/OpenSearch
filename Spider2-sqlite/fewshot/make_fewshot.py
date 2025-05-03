prompt = """
Given a Text-to-SQL task and database info, you are asked to generate 10 fewshot examples related to this task based on DB info. The answer format should be:
/* Some SQL examples are provided based on similar problems: */
/* Answer the following: Q1 */
SELECT ...

/* Answer the following: Q2 */
SELECT ...

...

/* Answer the following: Q10 */
SELECT ...

The DB info is {0}.
Task: {1}.

Here is one example:

e.g.
/* Some SQL examples are provided based on similar problems: */
/* Answer the following: What is the highest infant mortality rate per thousand of the countries whose inflation is under 3? */
SELECT MAX(T2.Infant_Mortality) FROM economy AS T1 INNER JOIN population AS T2 ON T1.Country = T2.Country WHERE T1.Inflation < 3

/* Answer the following: List at least 5 students who has the longest absense from schoool? longest absense refers to MAX(month) */
SELECT name FROM longest_absense_from_school ORDER BY month DESC LIMIT 5

/* Answer the following: What is the number of unemployed and bankrupt students? */
SELECT COUNT(T1.name) FROM unemployed AS T1 INNER JOIN filed_for_bankrupcy AS T2 ON T1.name = T2.name

/* Answer the following: What is the keyword for episodes with stars score of 10 at 30% and above? stars score of 10 at 30% and above refers to stars = 10 and percent > 29 */
SELECT T1.keyword FROM Keyword AS T1 INNER JOIN Vote AS T2 ON T1.episode_id = T2.episode_id WHERE T2.stars = 10 AND T2.percent > 29;

/* Answer the following: Tell the number of 4-year public schools in UT whose graduation rate exceeds the average for the state. 4-year refers to level = '4-year'; public refers to control = 'Public'; UT refers to state_abbr = 'UT'; graduation rate exceeds the average for the state refers to awards_per_value > awards_per_state_value; */
SELECT COUNT(DISTINCT T1.chronname) FROM institution_details AS T1 INNER JOIN state_sector_grads AS T2 ON T2.state = T1.state WHERE T2.state_abbr = 'UT' AND T1.level = '4-year' AND T1.control = 'Public' AND T1.awards_per_value > T1.awards_per_state_value

/* Answer the following: In the state with the highest state appropriations to higher education in fiscal year 2011 per resident, which institution has the lowest number of undergraduates in 2010? highest state appropriations to higher education in fiscal year 2011 per resident refers to MAX(state_appr_value); lowest number of undergraduates refers to MIN(student_count); in 2010 refers to year = 2010; */
SELECT T1.chronname FROM institution_details AS T1 INNER JOIN state_sector_details AS T2 ON T2.state = T1.state INNER JOIN institution_grads AS T3 ON T3.unitid = T1.unitid WHERE T1.student_count = (
    SELECT MIN(T1.student_count) FROM institution_details AS T1 INNER JOIN state_sector_details AS T2 ON T2.state = T1.state INNER JOIN institution_grads AS T3 ON T3.unitid = T1.unitid WHERE T3.year = 2010
) AND T3.year = 2010 GROUP BY T1.state ORDER BY SUM(T2.state_appr_value) DESC LIMIT 1

/* Answer the following: Give the level of education and occupation of customers ages from 20 to 35 with an income K of 2000 and below. customers ages from 20 to 35 refer to ID where age BETWEEN 20 AND 35; income K of 2000 and below refers to INCOME_K < 2000; level of education refers to EDUCATIONNUM; */
SELECT T1.EDUCATIONNUM, T1.OCCUPATION FROM Customers AS T1 INNER JOIN Demog AS T2 ON T1.GEOID = T2.GEOID WHERE T2.INCOME_K < 2000 AND T1.age >= 20 AND T1.age <= 35

/* Answer the following: Which institute has the highest percentage of male White students graduating in 2011 within 150 percent of normal/expected time? male refers to gender = 'M'; white refers to race = 'w'; in 2011 refers to year = 2011; graduating within 150 percent of normal/expected time refers to grad_150; */
SELECT T1.chronname FROM institution_details AS T1 INNER JOIN institution_grads AS T2 ON T2.unitid = T1.unitid WHERE T2.year = 2011 AND T2.gender = 'M' AND T2.race = 'W' AND T2.grad_150 = (
    SELECT MAX(T2.grad_150) FROM institution_details AS T1 INNER JOIN institution_grads AS T2 ON T2.unitid = T1.unitid WHERE T2.year = 2011 AND T2.gender = 'M' AND T2.race = 'W'
)

/* Answer the following: What is the total number of students in the school? */
SELECT COUNT(name) FROM person
"""