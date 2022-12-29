#include "precomp.hpp"

namespace cv
{
    Tracker::~Tracker(){}
    bool Tracker::init(InputArray image, const Rect2d& boundingBox)
    {
        if( isInit )
        {
            return false;
        }
        if( image.empty() )
            return false;
        sampler = Ptr<Tracker>
    }
}