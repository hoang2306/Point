#include "header/Object.hpp"

Object::Object(bool evil, double x,double y, double len)
{
    posn.x = x;
    posn.y = y;
    this->len = len;
    this->evil = evil;
}

void Object::UpdatePosn()
{
    double deltaTime = 1;
    velocity.Vx = velocity.Vx + acceleration.Ax*deltaTime; // vx = v0_x + a_x*t
    posn.x = posn.x + velocity.Vx*deltaTime; // x = x0 + vx*t
    velocity.Vy = velocity.Vy + acceleration.Ay*deltaTime; // vy = v0_y + a_y*t
    posn.y = posn.y + velocity.Vy*deltaTime; // y = y0 + vy*t
}

//getters
double Object::getLen(){return len;}
Vec2 Object::getPosn(){return posn;}
Vel2 Object::getVel(){return velocity;}
Acc2 Object::getAcc(){return acceleration;}

//setters
void Object::setAcc_x(double acc){acceleration.Ax = acc;}
void Object::setAcc_y(double acc){acceleration.Ay = acc;}
void Object::setPosn_x(double x){posn.x = x;}
void Object::setPosn_y(double y){posn.y = y;}
void Object::setVel_x(double velx){velocity.Vx = velx;}
void Object::setVel_y(double vely){velocity.Vy = vely;}
