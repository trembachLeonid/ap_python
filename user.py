from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from models import User, FamilyMemberRelation, Operation, Session, Family
from schemas import user_schema
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


user = Blueprint('user', __name__)
bcrypt = Bcrypt()
session = Session()

#works
@user.route('/user', methods=['POST'])
def new_user():
    data = request.json

    try:
        user_schema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 405

    exists = session.query(User).filter_by(username=data['username']).first()
    if exists:
        return Response(status=400, response='User with such username already exists.')

    exists = session.query(User).filter_by(phone=data['phone']).first()
    if exists:
        return Response(status=400, response='Phone was already taken')

    exists = session.query(User).filter_by(email=data['email']).first()
    if exists:
        return Response(status=400, response='This email was already taken')

    new_user = User(username=data['username'], firstName=data['firstName'], lastName=data['lastName'],
                    password=bcrypt.generate_password_hash(data['password']),
                    email=data['email'], phone=data['phone'], currentMoney=data['currentMoney'])

    session.add(new_user)
    session.commit()
    session.close()

    return Response(response='New user was successfully created!')
#works
@user.route('/user/<userId>', methods=['GET'])
def get_user(userId):
    user_data = session.query(User).filter_by(id=userId).first()
    if not user_data:
        return Response(status=404, response='User was not found')

    user_data = {'id': user_data.id, 'username': user_data.username, 'firstName': user_data.firstName,
                 'lastName': user_data.lastName,
                 'email': user_data.email, 'phone': user_data.phone, 'currentMoney': user_data.currentMoney}
    return jsonify({"user": user_data})
#works
@user.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    data = request.get_json(force=True)
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    if not user:
        return Response(status=401, response='You are not allowed to do that')
    try:
        user_schema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 405
    user_data = session.query(User).filter_by(id=user.id).first()
    if 'username' in data.keys():
        exists = session.query(User).filter_by(username=data['username']).first()
        if exists:
            return Response(status=400, response='User with such username already exists.')
        user_data.username = data['username']
    if 'firstName' in data.keys():
        user_data.firstName = data['firstName']
    if "lastName" in data.keys():
        user_data.lastName = data['lastName']
    if 'password' in data.keys():
        hashed_password = bcrypt.generate_password_hash(data['password'])
        user_data.password = hashed_password
    if 'email' in data.keys():
        exists = session.query(User).filter_by(email=data['email']).first()
        if exists:
            return Response(status=400, response='Email is already taken')
        user_data.email = data['email']
    if 'phone' in data.keys():
        exists = session.query(User).filter_by(phone=data['phone']).first()
        if exists:
            return Response(status=400, response='Phone is already taken')
        user_data.phone = data['phone']

    session.commit()
    session.close()
    return Response( response='User updated')
#works
@user.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    userId = user.id
    if not user:
        return Response(status=401, response='You are not allowed to do that')
    user_data = session.query(User).filter_by(id=userId).first()
    families = session.query(FamilyMemberRelation).filter_by(userId=userId)
    operations = session.query(Operation).filter_by(userId=userId)
    if families is not None:
        for fam in families:
            session.delete(fam)
    if operations is not None:
        for op in operations:
            session.delete(op)
    session.delete(user_data)
    session.commit()
    session.close()
    return Response(response='User was deleted')
#works
@user.route('/user/getFamilyList', methods=['GET'])
@jwt_required()
def get_user_families():
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    if not user:
        return Response(status=401, response='You are not allowed to do that')
    familiesIds = session.query(FamilyMemberRelation).filter_by(userId=user.id)
    if not familiesIds:
        return Response(response='This user has no families yet')
    output = []
    for i in familiesIds:
        temp = session.query(Family).filter_by(id=i.familyId).first()
        output.append({"id":temp.id,"familyName":temp.familyName,"currentMoney":temp.currentMoney})
    return jsonify({"Families": output})