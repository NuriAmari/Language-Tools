//
// Created by Nuri Amari on 2020-07-05.
//

#include <string>
#include "gtest/gtest.h"
#include "lexer/DFA.h"
#include "lexer/NFA.h"

class NFAFixture : public ::testing::Test {
protected:
    virtual void SetUp()
    {
        a = new DFA{Atom{'a'}};
    }

    virtual void TearDown() {
        delete a;
    }

    DFA*a ;
};

TEST_F(NFAFixture, SingleCharacter) {
    EXPECT_EQ(a->match("a"), 1);
}

