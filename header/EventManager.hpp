
#ifndef EventManager_hpp
#define EventManager_hpp

#include <stdio.h>
#include <vector>

#include "Rope.hpp"
#include "RenderWindow.h"
#include "Me.hpp"
#include "Object.hpp"
#include <SDL.h>
#include <SDL_image.h>

class eventManager{
public:
    bool Exit_MouseClick(int x, int y, int text_y, int text_width, int scr_width);
    bool Play_MouseClick(int x, int y, int text_width, int scr_width);
    bool Retry_MouseClick(int x, int y, int text_width, int scr_width);
    bool MouseClick(SDL_MouseButtonEvent& b, Rope* aRope, Me* mainObject, std::vector<Object*> enemyList, std::vector<Object*> frendList);
};

#endif
