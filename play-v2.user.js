(function () {
    var tdtoremove = document.querySelector('td');
    tdtoremove.parentNode.removeChild(tdtoremove);
})();

/**
 * 
 * @param {number} ms 
 * @returns {Promise<number>}
 */
function async_sleep(s) {
    return new Promise((resolve, _) => setTimeout(resolve, s * 1000));
}

var keys_to_press = [];
window.get_keys_to_press = function () {
    var ktp = keys_to_press;
    keys_to_press = [];
    return ktp;
};

(async function () {
    while (document.querySelector('#game-container') === null)
        await async_sleep(0.1);
    keys_to_press.push(".");  // unmute tab
    while (document.querySelector('#logo')?.style?.display !== 'block')
        await async_sleep(0.1);
    await async_sleep(1.5);
    keys_to_press.push('1');
    await async_sleep(0.1);
    while (1) {
        var enemies = [...document.querySelectorAll('.enemy:not(.under-attack):not([data-marked=true])')];
        for (var enemy of enemies) {
            enemy.setAttribute('data-marked', 'true');
            var nbr = parseInt(enemy.innerText.trim(), 16);
            for (var i = 0; i < 8; i++)
                if ((1 << i) & nbr)
                    keys_to_press.push(String(8 - i));
        }
        if (enemies.length <= 0) await async_sleep(0.1);
    }
})();
