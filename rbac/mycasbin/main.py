
from typing import Optional
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import casbin
from pydantic import BaseModel



e = casbin.Enforcer("./rbac_model.conf", "./rbac_policy.csv")
def main():
    print("Hello from casbin!")
    sub= "admin"
    obj= "data1"
    act= "read"

    print(e.enforce(sub, obj, act))
    sub= "admin"
    obj= "/api/v1/oss/getLinkByResourceName"
    act= "get"
    print(e.enforce(sub, obj, act))


def check_permission(sub, obj, act)->bool:
    return e.enforce(sub, obj, act)






# 
# g,admin,user,
# g,admin,guest,
# g,user,guest,
# g,user1,guest,
# 
# 模拟数据库
fake_users_db = {
    "admin": { # 管理员
        "username": "admin",
        "full_name": "admin",
        "email": "admin@example.com",
        "hashed_password": "admin",
        "disabled": False,
    },
    "user": { # 用户
        "username": "user",
        "full_name": "user",
        "email": "user@example.com",
        "hashed_password": "user",
        "disabled": True,
    },
    "user1": { # 游客
        "username": "user1",
        "full_name": "user1",
        "email": "user1@example.com",
        "hashed_password": "user1",
        "disabled": True,
    },
}

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 模拟 hash 加密算法
def fake_hash_password(password: str) -> str:
    return password


# 返回给客户端的 User Model，不需要包含密码
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


# 继承 User，用于密码验证，所以要包含密码
class UserInDB(User):
    hashed_password: str


# OAuth2 获取 token 的请求路径
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    user_dict = fake_users_db.get(username)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码不正确")

    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码不正确")

    # 7、用户名、密码验证通过后，返回一个 JSON
    return {"access_token": user.username, "token_type": "bearer"}


# 模拟从数据库中根据用户名查找用户
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# 模拟验证 token，验证通过则返回对应的用户信息
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


# 根据当前用户的 token 获取用户，token 已失效则返回错误码
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# 判断用户是否活跃，活跃则返回，不活跃则返回错误码
async def get_current_active_user(user: User = Depends(get_current_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User")
    return user


# 接口列表
# /api/v1/user/login
# /api/v1/user/logout
# /api/v1/user/register
# /api/v1/user/userinfo
# /api/v1/admin/users
# /api/v1/admin/userUpdate
# /api/v1/admin/deleteUser
# /api/v1/posts/posts
# /api/v1/posts/postDetail
# /api/v1/posts/updatePost
# /api/v1/posts/post
# /api/v1/posts/deletePost
# /api/v1/tag/getPostByTags
# /api/v1/tag/getTags
# /api/v1/tag/addTag
# /api/v1/tag/deleteTag
# /api/v1/comments/getCommentsByPostIdLikeTree
# /api/v1/comments/getCommentsByPostId
# /api/v1/comments/addComment
# /api/v1/comments/replyComment
# /api/v1/comments/deleteComment
# /api/v1/comments/likeComment
# /api/v1/comments/dislikeComment
# /api/v1/comments/getAllComments
# /api/v1/comments/changeCommentStat
# /api/v1/oss/uploadAndGetLink
# /api/v1/stats/events
# /api/v1/stats/visits
# /api/v1/overview
# /api/v1/oss/getResources
# /api/v1/oss/getLinkByResourceName
# /api/v1/comments/updateComment
# /api/v1/user/checkUserAdmin
@app.get("/api/v1/user/login")
async def login(user: User = Depends(get_current_active_user)):
    return user

@app.get("/api/v1/user/logout")
async def logout(user: User = Depends(get_current_active_user)):
    return user

@app.get("/api/v1/user/register")
async def register(user: User = Depends(get_current_active_user)):
    return user


# 获取当前用户信息
@app.get("/user/me")
async def read_user(user: User = Depends(get_current_active_user)):
    return user

@app.get("/api/v1/admin/users")
async def users(user: User = Depends(get_current_active_user)):
    is_active = check_permission(user.username, "/api/v1/admin/users", "get")
    if not is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return user







if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="127.0.0.1", port=8080)