#include "solver.h"

Solver::Solver(vvector first_puzzle)
{
    this->psize = static_cast<int>(first_puzzle.size());
    this->generate_solution();
    this->compute_targets();
    this->ppuzzle = first_puzzle;
}

Solver::~Solver()
{
}

Solver::node Solver::solve(void)
{
    this->opened.push({this->compute_score(this->ppuzzle), {}, this->ppuzzle, 0});
    return (this->astar());
}

void Solver::compute_targets(void)
{
    this->ptargets.push_back({-1, -1});
    for (int i = 1; i < this->psize * this->psize; i++)
    {
        this->ptargets.push_back(this->find_value(this->psolution, i));
    }
}

void Solver::generate_solution(void)
{
    for (int i = 0; i < this->psize; i++)
    {
        this->psolution.push_back(std::vector<int>());
        for (int j = 0; j < this->psize; j++)
        {
            this->psolution[i].push_back(0);
        }
    }
    int tmp = 0, x = 0, y = 0, dx = 0, dy = 1;
    for (int i = 1; i < this->psize * this->psize; i++)
    {
        this->psolution[x][y] = i;
        if (x + dx < 0 || x + dx >= this->psize || y + dy < 0 || y + dy >= this->psize || this->psolution[x + dx][y + dy] != 0)
        {
            tmp = dx;
            dx = dy;
            dy = -tmp;
        }
        x += dx;
        y += dy;
    }
}

void Solver::print_array(vvector array)
{
    int len = static_cast<int>(array.size());
    for (int i = 0; i < len; i++)
    {
        for (int j = 0; j < len; j++)
        {
            std::cout << array[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

int Solver::manhattan(std::tuple<int, int> target, std::tuple<int, int> coords)
{
    return abs(std::get<0>(target) - std::get<0>(coords)) + abs(std::get<1>(target) - std::get <1>(coords));
}

int Solver::linear_conflict(vvector array, std::tuple<int, int> target, std::tuple<int, int> coords)
{
    int score;
    int direction;

    score = this->manhattan(target, coords);
    if (std::get<0>(coords) == std::get<0>(target))
    {
        direction = 2 * (std::get<1>(target) > std::get<1>(coords)) - 1;
        for (int x = (std::get<1>(coords) + direction); x < std::get<1>(target); x += direction)
        {
            if (std::get<0>(this->ptargets[array[std::get<0>(coords)][x]]) == std::get<0>(target))
                return score + 2;
        }
    }
    if (std::get<1>(coords) == std::get<1>(target))
    {
        direction = 2 * (std::get<0>(target) > std::get<0>(coords)) - 1;
        for (int x = (std::get<0>(coords) + direction); x < std::get<0>(target); x += direction)
        {
            if (std::get<1>(this->ptargets[array[std::get<1>(coords)][x]]) == std::get<1>(target))
                return score + 2;
        }
    }
    return score;
}

int Solver::compute_score(vvector array)
{
    int score = 0;
    std::tuple<int, int> target;

    for (int x = 0; x < this->psize; x++)
    {
        for (int y = 0; y < this->psize; y++)
        {
            target = this->ptargets[array[x][y]];
            if (array[x][y] != 0 && x != std::get<0>(target) && y != std::get<1>(target))
                score += this->linear_conflict(array, target, {x, y});
        }
    }
    return score;
}

std::tuple<int, int> Solver::find_value(vvector array, int value)
{
    for (int x = 0; x < this->psize; x++)
    {
        for (int y = 0; y < this->psize; y++)
        {
            if (array[x][y] == value)
            {
                return {x, y};
            }
        }
    }
    return {-1, -1};
}

Solver::node Solver::astar(void)
{
    size_t max_state = 0;
    while (this->opened.size() > 0)
    {
        max_state = std::max(max_state, this->opened.size());
        node current_node = this->opened.top();
        if (std::hash<vvector>()(std::get<2>(current_node)) == std::hash<vvector>()(this->psolution))
            return current_node;
        if (std::get<1>(this->closed.insert(std::get<2>(current_node))) == false){
            this->opened.pop();
            continue;
        }
        std::tuple<int, int> w = this->find_value(std::get<2>(current_node), 0);
        if (std::get<1>(w) > 0)
            this->opened.push(this->slide_left(current_node));
        if (std::get<1>(w) < this->psize - 1)
            this->opened.push(this->slide_right(current_node));
        if (std::get<0>(w) > 0)
            this->opened.push(this->slide_up(current_node));
        if (std::get<0>(w) < this->psize - 1)
            this->opened.push(this->slide_down(current_node));
        this->opened.pop();
    }
    return this->opened.top();
}

Solver::node Solver::slide_left(node current_node)
{
    std::tuple<int, int> w = this->find_value(std::get<2>(current_node), 0);
    node new_node(current_node);
    vvector arr = std::get<2>(new_node);
    std::swap(arr[std::get<0>(w)][std::get<1>(w)], arr[std::get<0>(w)][std::get<1>(w) - 1]);
    std::get<0>(new_node) = this->compute_score(std::get<2>(new_node)) + std::get<1>(new_node).size();
    std::get<1>(new_node).push_back(SLIDE_LEFT);
    std::get<2>(new_node) = arr;
    return new_node;
}

Solver::node Solver::slide_up(node current_node)
{
    std::tuple<int, int> w = this->find_value(std::get<2>(current_node), 0);
    node new_node(current_node);
    vvector arr = std::get<2>(new_node);
    std::swap(arr[std::get<0>(w)][std::get<1>(w)], arr[std::get<0>(w) - 1][std::get<1>(w)]);
    std::get<0>(new_node) = this->compute_score(std::get<2>(new_node)) + std::get<1>(new_node).size();
    std::get<1>(new_node).push_back(SLIDE_UP);
    std::get<2>(new_node) = arr;
    return new_node;
}

Solver::node Solver::slide_right(node current_node)
{
    std::tuple<int, int> w = this->find_value(std::get<2>(current_node), 0);
    node new_node(current_node);
    vvector arr = std::get<2>(new_node);
    std::swap(arr[std::get<0>(w)][std::get<1>(w)], arr[std::get<0>(w)][std::get<1>(w) + 1]);
    std::get<0>(new_node) = this->compute_score(std::get<2>(new_node)) + std::get<1>(new_node).size();
    std::get<1>(new_node).push_back(SLIDE_RIGHT);
    std::get<2>(new_node) = arr;
    return new_node;
}

Solver::node Solver::slide_down(node current_node)
{
    std::tuple<int, int> w = this->find_value(std::get<2>(current_node), 0);
    node new_node(current_node);
    vvector arr = std::get<2>(new_node);
    std::swap(arr[std::get<0>(w)][std::get<1>(w)], arr[std::get<0>(w) + 1][std::get<1>(w)]);
    std::get<0>(new_node) = this->compute_score(std::get<2>(new_node)) + std::get<1>(new_node).size();
    std::get<1>(new_node).push_back(SLIDE_DOWN);
    std::get<2>(new_node) = arr;
    return new_node;
}