from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from models import Family, FamilyMemberRelation, Operation, User, Session
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


history = Blueprint('history', __name__)
session = Session()

#works
@history.route('/history', methods=['GET'])
@jwt_required()
def get_user_history():
    logged = get_jwt_identity()
    user = session.query(User).filter_by(username=logged).first()
    if not user:
        return Response(status=401, response='You are not allowed to do that')
    operations = session.query(Operation).filter_by(userId=id)
    operationjson = {}
    for op in operations:
        operationjson += {'id': op.id,
                          'family': session.query(Family).
                                          filter_by(id=op.familyId).first().familyName,
                          'moneyChange': op.moneyChange}
    return jsonify({'userHistory': operationjson})
#works
@history.route('/history/<id>', methods=['GET'])
@jwt_required()
def get_family_history(id):
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
    operations = session.query(Operation).filter_by(familyId=id)
    operationjson = []
    for op in operations:
        operationjson.append({'id': op.id,
                          'familyMember': session.query(User).
                                          filter_by(id=op.userId).first().username,
                          'moneyChange': op.moneyChange})
    return jsonify({'familyHistory': operationjson})