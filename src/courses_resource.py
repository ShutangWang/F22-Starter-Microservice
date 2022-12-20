import pymysql


class CoursesResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        conn = pymysql.connect(
            user="root",
            password="dbuserdbuser",
            host="database-course.ctpmijmek5ds.us-east-1.rds.amazonaws.com",
            # host="localhost",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_userid(user_id):
        sql = "SELECT * FROM cc_courses.cc_courses where user_id=%s";
        conn = CoursesResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=user_id)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_by_teacherid(teacher_id):
        sql = "SELECT * FROM cc_courses.cc_courses where teacher_id=%s";
        conn = CoursesResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=teacher_id)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_courses():
        sql = "SELECT * FROM cc_courses.cc_courses";
        conn = CoursesResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()

        return result

    @staticmethod
    def create_course_by_field(fields):
        insert_sql = """
            insert into cc_courses.cc_courses(user_id,teacher_id,create_time,appointment_time,price)
            values("%s","%s","%s","%s",%f);
        """
        last_id_sql = "select last_insert_id() from cc_courses.cc_courses limit 1;"

        sql = insert_sql % fields
        print(sql)
        conn = CoursesResource._get_connection()
        cur = conn.cursor()

        res = cur.execute(sql)
        cur.execute(last_id_sql)
        for row in cur:
            return row['last_insert_id()']

