from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from models import Family, FamilyMemberRelation, Operation, User, Session
from schemas import family_schema
from datetime import datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


family = Blueprint('family', __name__)
session = Session()
#works
@family.route('/family', methods=['POST'])
@jwt_required()
def add_family():
    data = request.get_json(force=True)

    try:
        family_schema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    if not user:
        return Response(status=401, response='You are not allowed to do this')
    for i in data['users']:
        if user.username == i:
            return Response(status=400, response='You cannot pass yourself as parameter')
        usr = session.query(User).filter_by(username=i).first()
        if not usr:
            return Response(status=404, response='Provided user data was not found')
    exists = session.query(Family).filter_by(familyName=data['familyName']).first()
    if exists:
        return Response(status=400, response='Family with such name already exists')
    new_family = Family(familyName=data['familyName'], currentMoney=0)
    session.add(new_family)
    for i in data['users']:
        usr = session.query(User).filter_by(username=i).first()
        session.add(FamilyMemberRelation(userId=usr.id, familyId=new_family.id))
    session.add(FamilyMemberRelation(userId=user.id, familyId=new_family.id))
    session.commit()
    session.close()
    return Response(response='New family was successfully created!')
#works
@family.route('/family/<id>', methods=['PUT'])
@jwt_required()
def update_family(id):
    data = request.get_json(force=True)
    try:
        family_schema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    family = session.query(Family).filter_by(id=id).first()
    if not family:
        return Response(status=404, response='Family was not found')
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    if not user:
        return Response(status=401, response='You are not allowed to do that')
    members = session.query(FamilyMemberRelation).filter_by(familyId=id)
    checkId = []
    for i in members:
        checkId.append(i.userId)
    if not user.id in checkId:
        return Response(status=401, response='You are not allowed to do that')
    if 'users' in data.keys():
        for i in data['users']:
            if user.username == i:
                return Response(status=400, response='You cannot pass yourself as parameter')
            usr = session.query(User).filter_by(username=i).first()
            if not usr:
                return Response(status=404, response='Provided user data was not found')
            if usr.id in checkId:
                return Response(status=400, response='One of the users is already here')
    if 'familyName' in data.keys():
        exists = session.query(Family).filter_by(familyName=data['familyName']).first()
        if exists:
            return Response(status=400, response='Family with such name already exists')

    if 'familyName' in data.keys():
        family.familyName = data['familyName']
    if 'users' in data.keys():
        for user in data['users']:
            usr = session.query(User).filter_by(username=user).first()
            session.add(FamilyMemberRelation(userId=usr.id, familyId=family.id))
    session.commit()
    session.close()
    return Response(response="Family has been updated")
#works
@family.route('/family/<id>', methods=['DELETE'])
@jwt_required()
def delete_family(id):
    family = session.query(Family).filter_by(id=id).first()
    if not family:
        return Response(status=404, response="Family does not exist")
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    if not user:
        return Response(status=401, response='You are not allowed to do that')
    memberIds = session.query(FamilyMemberRelation).filter_by(familyId=id)
    checkId = []
    for i in memberIds:
        checkId.append(i.userId)
    if not user.id in checkId:
        return Response(status=401, response='You are not allowed to do that')
    users = session.query(FamilyMemberRelation).filter_by(familyId=id)
    operations = session.query(Operation).filter_by(familyId=id)
    if memberIds is not None:
        for m in memberIds:
            session.delete(m)
    if operations is not None:
        for o in operations:
            session.delete(o)
    if users is not None:
        for u in users:
            session.delete(u)
    session.delete(family)
    session.commit()
    session.close()
    return Response(response='Family was deleted')
#works
@family.route('/family/account/<id>', methods=['GET'])
@jwt_required()
def get_account_info(id):
    family = session.query(Family).filter_by(id=id).first()
    if not family:
        return Response(status=404, response="Family does not exist")
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    if not user:
        return Response(status=401, response='You are not allowed to do that')
    memberIds = session.query(FamilyMemberRelation).filter_by(familyId=id)
    checkId = []
    for i in memberIds:
        checkId.append(i.userId)
    if not user.id in checkId:
        return Response(status=401, response='You are not allowed to do that')
    family = {'id': family.id, 'currentMoney': family.currentMoney}
    return jsonify({'family': family})
#works
@family.route('/family/account/<id>', methods=['PUT'])
@jwt_required()
def make_transaction(id):
    data = request.get_json(force=True)
    family = session.query(Family).filter_by(id=id).first()
    if not family:
        return Response(status=404, response="Family does not exist")
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    if not user:
        return Response(status=401, response='You are not allowed to do that')
    memberIds = session.query(FamilyMemberRelation).filter_by(familyId=id)
    checkId = []
    for i in memberIds:
        checkId.append(i.userId)
    if not user.id in checkId:
        return Response(status=401, response='You are not allowed to do that')
    user.currentMoney -= data['money']
    family.currentMoney += data['money']
    operation = Operation(id=None, userId=user.id, familyId=family.id, moneyChange=data['money'], date=datetime.utcnow())
    session.add(operation)
    session.commit()
    session.close()
    return Response(response="Transaction completed")
