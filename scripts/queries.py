# SQL queries mapped to Prisma schema database tables

GET_USER_METRICS = """
SELECT 
    role,
    status,
    COUNT(*) as count
FROM users
GROUP BY role, status;
"""

GET_USER_GROWTH = """
SELECT 
    DATE_TRUNC('month', "createdAt") as month,
    COUNT(*) as new_users
FROM users
GROUP BY month
ORDER BY month;
"""

GET_COURSE_PERFORMANCE = """
SELECT 
    c.id,
    c.title,
    c.price,
    c."isPublished",
    COUNT(e.id) as total_enrollments,
    COALESCE(AVG(r.rating), 0) as average_rating,
    COALESCE(SUM(p.amount), 0) as total_revenue
FROM courses c
LEFT JOIN enrollments e ON c.id = e."courseId"
LEFT JOIN reviews r ON c.id = r."courseId"
LEFT JOIN payments p ON c.id = p."courseId" AND p.status = 'COMPLETED'
WHERE c."isDeleted" = false
GROUP BY c.id, c.title, c.price, c."isPublished"
ORDER BY total_enrollments DESC;
"""

GET_REVENUE_METRICS = """
SELECT 
    status,
    type,
    SUM(amount) as total_amount,
    COUNT(*) as payment_count
FROM payments
GROUP BY status, type;
"""

GET_REVENUE_OVER_TIME = """
SELECT 
    DATE_TRUNC('day', "createdAt") as date,
    SUM(amount) as daily_revenue
FROM payments
WHERE status = 'COMPLETED'
GROUP BY date
ORDER BY date;
"""

GET_LIVE_SESSION_METRICS = """
SELECT 
    title,
    level,
    "sessionDate",
    "maxCapacity",
    COUNT(r.id) as registrations_count
FROM live_sessions ls
LEFT JOIN live_registrations r ON ls.id = r."sessionId"
GROUP BY ls.id, title, level, "sessionDate", "maxCapacity"
ORDER BY "sessionDate" DESC;
"""
