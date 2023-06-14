var loading_timer;
var galleryblockextension = '.html';
var galleryblockdir = 'galleryblock';
var nozomiextension = '.nozomi';
var gg = {};
var is_safari = false;//['iPad Simulator', 'iPhone Simulator', 'iPod Simulator', 'iPad', 'iPhone', 'iPod'].includes(navigator.platform) || (navigator.userAgent.includes("Mac") && "ontouchend" in document);///(\s|^)AppleWebKit\/[\d\.]+\s+\(.+\)\s+Version\/(1[0-9]|[2-9][0-9]|\d{3,})(\.|$|\s)/i.test(navigator.userAgent);

function subdomain_from_url(url, base) {
        var retval = 'b';
        if (base) {
                retval = base;
        }
        
        var b = 16;
        
        var r = /\/[0-9a-f]{61}([0-9a-f]{2})([0-9a-f])/;
        var m = r.exec(url);
        if (!m) {
                return 'a';
        }
        
        var g = parseInt(m[2]+m[1], b);
        if (!isNaN(g)) {
                retval = String.fromCharCode(97 + gg.m(g)) + retval;
        }
        
        return retval;
}

function url_from_url(url, base) {
        return url.replace(/\/\/..?\.hitomi\.la\//, '//'+subdomain_from_url(url, base)+'.hitomi.la/');
}


function full_path_from_hash(hash) {
        return gg.b+gg.s(hash)+'/'+hash;
}

function real_full_path_from_hash(hash) {
        return hash.replace(/^.*(..)(.)$/, '$2/$1/'+hash);
}


function url_from_hash(galleryid, image, dir, ext) {
        ext = ext || dir || image.name.split('.').pop();
        dir = dir || 'images';
        
        return 'https://a.hitomi.la/'+dir+'/'+full_path_from_hash(image.hash)+'.'+ext;
}

function url_from_url_from_hash(galleryid, image, dir, ext, base) {
        if ('tn' === base) {
                return url_from_url('https://a.hitomi.la/'+dir+'/'+real_full_path_from_hash(image.hash)+'.'+ext, base);
        }
        return url_from_url(url_from_hash(galleryid, image, dir, ext), base);
}

function rewrite_tn_paths(html) {
        return html.replace(/\/\/tn\.hitomi\.la\/[^\/]+\/[0-9a-f]\/[0-9a-f]{2}\/[0-9a-f]{64}/g, function(url) {
                return url_from_url(url, 'tn');
        });
}



console.log(subdomain_from_url('18df50f9540ce9c3200c84860f29bdb1bbd4c20cb38becab12624196b5e819e1',16))