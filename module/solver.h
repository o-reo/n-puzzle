#pragma once
#include <vector>
#include <iostream>
#include <tuple>
#include <queue>
#include <algorithm>
#include <unordered_set>
#include <functional>

namespace std
{

template <>
class hash<std::vector<std::vector<int>>>
{
public:
    size_t operator()(const std::vector<std::vector<int>> &s) const
    {
        std::string str;
        for (size_t i = 0; i < s.size(); i++)
        {
            for (size_t j = 0; j < s.size(); j++)
            {
                str += std::to_string(s[i][j]);
            }
        }
        return std::hash<std::string>()(str);
    }
};

template <>
class equal_to<std::vector<std::vector<int>>>
{
public:
    size_t operator()(const std::vector<std::vector<int>> &v1, const std::vector<std::vector<int>> &v2) const
    {
        for (size_t i = 0; i < v1.size(); i++)
        {
            for (size_t j = 0; j < v1.size(); j++)
            {
                if (v1[i][j] != v2[i][j])
                    return false;
            }
        }
        return true;
    }
};

} // namespace std

class Solver
{
    typedef std::vector<std::vector<int>> vvector;
    enum SLIDES
    {
        SLIDE_LEFT,
        SLIDE_UP,
        SLIDE_RIGHT,
        SLIDE_DOWN
    };
    typedef std::tuple<int, std::vector<SLIDES>, vvector, int> node;

public:
    Solver(vvector first_puzzle);
    ~Solver(void);
    void generate_solution(void);
    node solve(void);
    void print_array(vvector array);
    int compute_score(vvector array);
    int linear_conflict(vvector array, std::tuple<int, int> target, std::tuple<int, int> coords);
    int manhattan(std::tuple<int, int> target, std::tuple<int, int> coords);
    int hamming(std::tuple<int, int> target, std::tuple<int, int> coords);
    node astar(void);
    std::tuple<int, int> find_value(vvector array, int value);
    node slide_left(node current_node);
    node slide_right(node current_node);
    node slide_up(node current_node);
    node slide_down(node current_node);
    void compute_targets(void);

private:
    int psize;
    vvector psolution;
    std::vector<std::tuple<int, int>> ptargets;
    std::priority_queue<node, std::vector<node>, std::greater<node> > opened;
    std::unordered_set<std::vector<std::vector<int>>> closed;
    vvector ppuzzle;
};