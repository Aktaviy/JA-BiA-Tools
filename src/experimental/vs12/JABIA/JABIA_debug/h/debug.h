/*
@author: sbobovyc
*/

/*
Copyright (C) 2013 Stanislav Bobovych

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef DEBUG
#define DEBUG
#include <windows.h>
#include <boost/archive/xml_oarchive.hpp> 
#include <boost/archive/xml_iarchive.hpp> 
#include <boost/serialization/vector.hpp>
#include <iostream> 
#include <fstream> 
#include "character.h"
#include "game_version.h"

#ifdef JABIA_EXPORTS
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __declspec(dllimport)
#endif

#define FULL

typedef void * (_stdcall *CharacterConstReturnPtr)();
typedef void * (_stdcall *UpdateCharacterExpPtr)();
typedef void * (_stdcall *CharacterDestReturnPtr)();
typedef int (_stdcall *CharacterDestructorPtr)(JABIA_Character *);
typedef void * (_fastcall *WeaponReturnPtr)();

#ifdef __cplusplus
extern "C" {
#endif 

EXPORT BOOL CALLBACK DialogProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);
#ifdef __cplusplus
}
#endif


DWORD WINAPI MyThread(LPVOID);
// my hooks
void* myCharacterConstReturn();
void* myCharacterDestReturn();
void* mySaveGameParseReturn();
void* myWeaponConstReturn();
void __fastcall recordCharacters(void* instance);
void __fastcall removeCharacter(JABIA_Character * ptr);
void __fastcall recordWeapons(void* instance);
int myCharacterDestructor(JABIA_Character * ptr);

// gui functions
void dump_current_character(HWND hwnd, JABIA_Character * ptr);
BOOL dump_all_characters(HWND hwnd);
void fillDialog(HWND hwnd, JABIA_Character * ptr);
void setCharacter(HWND hwnd, JABIA_Character * ptr, bool inventory_weapon_changed, bool equiped_weapon_changed);
void setMoney(HWND hwnd);

#define PATH_TO_DEBUGMOD_XML "\\mods\\debugger\\JABIA_debugger.xml"


class JABIA_DEBUGMOD_parameters { 
public:
	bool first_run;	


	// initializer list to use copy constructor instead of default constructor
    JABIA_DEBUGMOD_parameters() : 	
		first_run(true)
    {
	}
	
	
	
	// TODO add pretty print 
    friend std::ostream& operator << (std::ostream& out, JABIA_DEBUGMOD_parameters& d) 
    {
        /*out << "day: " << d.m_day 
              << " month: " << d.m_month
	<< " year: " << d.m_year;
        */return out;
    }

	// take care of serilization to xml
    template<class Archive>
    void serialize(Archive& archive, const unsigned int version)
    {
		archive & BOOST_SERIALIZATION_NVP(first_run);
    }
};


#endif /* DEBUG */