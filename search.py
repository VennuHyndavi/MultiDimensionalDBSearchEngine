import sys
import graphene
import mysql.connector as mysql

class Choice(graphene.ObjectType):
    value = graphene.String()
    no = graphene.Int()

class Domain(graphene.ObjectType):
    domainName = graphene.String()

class SearchCriteria(graphene.ObjectType):
    questionNumber = graphene.Int()
    question = graphene.String()
    questionType = graphene.String()
    options = graphene.List(Choice)

class GetResult(graphene.ObjectType):
    name = graphene.String()
    url = graphene.String()



class Queries(graphene.ObjectType):
    result = graphene.List(GetResult, options = graphene.List(graphene.List(graphene.Int)), domain= graphene.String())
    domainList = graphene.List(Domain)
    searchQuestions = graphene.List(SearchCriteria, domain = graphene.String())
    
    def resolve_domainList(self, info):
        db = mysql.connect(
            host="localhost",
            database="project",
            user="root",
            passwd="root",
            auth_plugin='mysql_native_password'
        )
        query = "select domainName from DOMAIN"
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        domainList = []
        for record in records:
            domainList.append(Domain(domainName=record[0]))
        return domainList

    def resolve_searchQuestions(self, info, domain):
        db = mysql.connect(
            host="localhost",
            database="project",
            user="root",
            passwd="root",
            auth_plugin='mysql_native_password'
        )
        query1 = "select *from PROPERTY where domainName='"+domain+"'"
        cursor = db.cursor()
        cursor.execute(query1)
        records1 = cursor.fetchall()
        query2 = "select propertyName,allowedValue,allowedValueCode from propertyDetail where domainName='"+domain+"'"
        cursor.execute(query2)
        records2 = cursor.fetchall()
        cursor.close()
        db.close()
        questions=[]
        for record in records1:
            question = record[1]
            option=[]
            print(question)
            for row in records2:
                if row[0]==question:
                    option.append(Choice(value=row[1],no=row[2]))
                    print(row[1],row[2])
            print(option)
            questions.append(SearchCriteria(questionNumber=record[3],question=record[2],questionType=record[4],options=option))
        
        newlist = sorted(questions, key=lambda x: x.questionNumber)

        return newlist

    def resolve_result(self, info, domain, options):
        db = mysql.connect(
            host="localhost",
            database="project",
            user="root",
            passwd="root",
            auth_plugin='mysql_native_password'
        )
        if domain == "Colleges":    
            query = "select *from collegeFactTable"
        else:
            query = "select *from autoFactTable"
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        results=[]
        print(records,options)
        for record in records:
            counter=2
            f=True
            for i in range(len(options)):
                option = options[i]
                if option[0]==0:
                    counter+=1
                    f=True
                elif record[counter] in option:
                    counter+=1
                    f=True
                else:
                    f=False
                    break
            if f:
                results.append(GetResult(name=record[0],url = record[1]))
        return results
#trial start
class ResultType(graphene.ObjectType):
    userid = graphene.String()
    domainName = graphene.String()
    bname = graphene.String()
    bookmark = graphene.String()

class CreateUser(graphene.Mutation):
    class Arguments:
        userid = graphene.String(required=True)

    success = graphene.Boolean()
    result = graphene.List(ResultType)
    def mutate(self, info, userid):
        db = mysql.connect(
            host="localhost",
            database="project",
            user="root",
            passwd="root",
            auth_plugin='mysql_native_password'
        )
        check_query = "SELECT userid FROM user WHERE userid = %s"
        cursor = db.cursor()
        cursor.execute(check_query, (userid,))
        records1 = cursor.fetchall()
        if not records1:
            query = "INSERT INTO user (userid) VALUES ('{}')".format(userid)
            cursor.execute(query)
            return CreateUser(success=True)
            
        cursor = db.cursor()
        check_query1 = "SELECT * FROM userbookmark WHERE userid = %s"
        cursor.execute(check_query1, (userid,))
        records2=cursor.fetchall()
        result = []
        for record in records2:
            result.append(ResultType(
                userid=record[0],
                domainName=record[1],
                bname=record[2],
                bookmark=record[3]
            ))
        db.commit()
        cursor.close()
        db.close()
        return CreateUser(success=True,result=result)
        #return CreateUser(resultList)

class UserBookmarkInput(graphene.InputObjectType):
    userId = graphene.Int()
    domain = graphene.String()
    bname = graphene.String()
    questionNumber = graphene.Int()
    question = graphene.String()
    questionType = graphene.String()
    options = graphene.List(graphene.Int)

class CreateUserBookmark(graphene.Mutation):
    class Arguments:
        input = UserBookmarkInput(required=True)

    success = graphene.Boolean()

    def mutate(self, info, input):
        db = mysql.connect(
            host="localhost",
            database="project",
            user="root",
            passwd="root",
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        # Check if user has less than 5 bookmarks
        check_query = "SELECT COUNT(*) FROM userbookmark WHERE userId = {}".format(input.userId)
        cursor.execute(check_query)
        count = cursor.fetchone()[0]
        if count >= 5:
            return CreateUserBookmark(success=False)
        query = "INSERT INTO userbookmark (userId, domain, questionNumber, question, questionType, options) VALUES ({}, '{}', {}, '{}', '{}', '{}')".format(input.userId, input.domain, input.questionNumber, input.question, input.questionType, options)
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        return CreateUserBookmark(success=True)

class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_user_bookmark = CreateUserBookmark.Field()

schema = graphene.Schema(query=Queries, mutation=Mutations)
#trial end
#schema = graphene.Schema(query=Queries)
########## CLIENT SIDE QUERIES  #########
# query{
#   domainList{
#     domainName
#   }
# }

# query{
#   searchQuestions(domain:"Colleges"){
#     question
#     questionType
#     questionNumber
#     options{
#       no
#       value
#     }
#   }
# }

# query{
#   result(domain:"Colleges", options:[[1],[1],[1,2,3],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]){
#    name
#     url
#   }
# }