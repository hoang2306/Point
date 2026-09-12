#include<SDL.h>
#include <SDL_image.h>
#include<iostream>
#include<SDL_ttf.h>

class LTexture
{
    public:

		LTexture();


		~LTexture();

		bool loadFromRenderedText(std::string textureText, SDL_Color textColor, SDL_Renderer* gRenderer, TTF_Font* gFont);


		void free();

		void render(int x, int y, SDL_Renderer* gRenderer);

		int getWidth();
		int getHeight();

	private:

		SDL_Texture* mTexture;


		int mWidth;
		int mHeight;
};
