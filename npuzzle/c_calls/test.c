/* ************************************************************************** */
/*                                                          LE - /            */
/*                                                              /             */
/*   test.c                                           .::    .:/ .      .::   */
/*                                                 +:+:+   +:    +:  +:+:+    */
/*   By: amatthys <amatthys@student.le-101.fr>      +:+   +:    +:    +:+     */
/*                                                 #+#   #+    #+    #+#      */
/*   Created: 2019/10/25 11:35:30 by amatthys     #+#   ##    ##    #+#       */
/*   Updated: 2019/10/25 12:11:08 by amatthys    ###    #+. /#+    ###.fr     */
/*                                                         /                  */
/*                                                        /                   */
/* ************************************************************************** */

#include <stdio.h>
#include <unistd.h>

void	print_puzzle(size_t *puzz, int size)
{
	write(1, "yo\n", 3);
	for (int i = 0; i < size; i++)
	{
		printf("%lu ", puzz[i]);
	}
}
